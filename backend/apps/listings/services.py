from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.db.transaction import atomic

from apps.cars.models import Brand, CarModel, ModelName
from apps.currency.models import CurrencyModel
from apps.listings.models import ListingModel
from core.enums.profanity_enum import ProfanityFilter
from core.services.managers_notification import ManagerNotificationService


PRICE_QUANT = Decimal('0.01')
MAX_EDIT_ATTEMPTS = 3


class ListingServiceError(Exception):
    def __init__(self, message: str, field: str | None = None):
        self.message = message
        self.field = field
        super().__init__(message)

    def as_dict(self):
        if self.field:
            return {self.field: self.message}

        return {'detail': self.message}


class ListingService:
    @staticmethod
    def get_managers():
        UserModel = get_user_model()

        return UserModel.objects.filter(
            is_staff=True,
            role__name='manager',
        )

    @staticmethod
    def notify_managers_about_profanity(*, description: str, seller):
        for manager in ListingService.get_managers():
            ManagerNotificationService.send_profanity_notification(
                description=description,
                username=seller.username,
                manager=manager,
            )

    @staticmethod
    def send_brand_request(*, brand_name: str, model_name: str | None, username: str) -> None:
        ManagerNotificationService.send_notification(
            brand_name=brand_name,
            model_name=model_name,
            username=username,
        )

    @staticmethod
    def increment_public_view(listing: ListingModel) -> None:
        listing.increment_views()

    @staticmethod
    def get_current_rate(currency):
        if not currency:
            return None

        current_currency = (
            CurrencyModel.objects
            .filter(currency_code=currency.currency_code)
            .order_by('-updated_at')
            .first()
        )

        return current_currency.rate if current_currency else getattr(currency, 'rate', None)

    @staticmethod
    def get_rates_map():
        return {
            item['currency_code']: Decimal(str(item['rate']))
            for item in CurrencyModel.objects.values('currency_code', 'rate')
        }

    @classmethod
    def calculate_converted_prices(cls, *, price: Decimal, currency) -> dict:
        rates = cls.get_rates_map()

        if not currency:
            return {
                'price_usd': Decimal('0.00'),
                'price_eur': Decimal('0.00'),
                'price_uah': Decimal('0.00'),
            }

        base_rate = rates.get(currency.currency_code, Decimal('1'))

        if base_rate == Decimal('0'):
            return {
                'price_usd': Decimal('0.00'),
                'price_eur': Decimal('0.00'),
                'price_uah': Decimal('0.00'),
            }

        def convert(target_code: str) -> Decimal:
            target_rate = rates.get(target_code, Decimal('1'))
            value = (price / base_rate) * target_rate

            return value.quantize(PRICE_QUANT, rounding=ROUND_HALF_UP)

        return {
            'price_usd': convert('USD'),
            'price_eur': convert('EUR'),
            'price_uah': convert('UAH'),
        }

    @staticmethod
    def get_or_create_car(*, brand: Brand, model_name: ModelName, body_type: str) -> CarModel:
        if model_name.brand_id != brand.id:
            raise ListingServiceError(
                message='Selected model does not belong to selected brand.',
                field='model_name',
            )

        car, _ = CarModel.objects.get_or_create(
            brand=brand,
            model_name=model_name,
            body_type=body_type,
        )

        return car

    @classmethod
    @atomic
    def create_listing(cls, *, data: dict, seller):
        brand = data.pop('brand')
        model_name = data.pop('model_name')
        body_type = data.pop('body_type')

        description = data.get('description', '')

        if ProfanityFilter.is_profane(description):
            cls.notify_managers_about_profanity(
                description=description,
                seller=seller,
            )
            raise ListingServiceError(
                message='The description contains prohibited words.',
                field='description',
            )

        car = cls.get_or_create_car(
            brand=brand,
            model_name=model_name,
            body_type=body_type,
        )

        currency = data['currency']
        price = data['price']

        converted_prices = cls.calculate_converted_prices(
            price=price,
            currency=currency,
        )

        return ListingModel.objects.create(
            car=car,
            seller=seller,
            active=True,
            initial_currency_rate=cls.get_current_rate(currency),
            **data,
            **converted_prices,
        )

    @classmethod
    @atomic
    def update_listing(cls, *, listing: ListingModel, data: dict):
        new_description = data.get('description')

        if new_description and ProfanityFilter.is_profane(new_description):
            listing.edit_attempts += 1

            update_fields = ['edit_attempts', 'updated_at']

            if listing.edit_attempts >= MAX_EDIT_ATTEMPTS:
                listing.active = False
                update_fields.append('active')

                cls.notify_managers_about_profanity(
                    description=new_description,
                    seller=listing.seller,
                )

                listing.save(update_fields=update_fields)

                raise ListingServiceError(
                    message='Maximum edit attempts exceeded. The listing has been deactivated.',
                    field='description',
                )

            listing.save(update_fields=update_fields)

            raise ListingServiceError(
                message='The description contains prohibited words.',
                field='description',
            )

        for field in (
            'title',
            'description',
            'listing_photo',
            'price',
            'currency',
            'region',
            'year',
            'engine',
        ):
            if field in data:
                setattr(listing, field, data[field])

        if 'price' in data or 'currency' in data:
            converted_prices = cls.calculate_converted_prices(
                price=listing.price,
                currency=listing.currency,
            )

            listing.price_usd = converted_prices['price_usd']
            listing.price_eur = converted_prices['price_eur']
            listing.price_uah = converted_prices['price_uah']

        listing.save()

        return listing

    @staticmethod
    def get_premium_stats(listing: ListingModel) -> dict:
        similar_by_region = ListingModel.objects.active().filter(
            car=listing.car,
            region=listing.region,
            price_usd__isnull=False,
        )
        similar_by_country = ListingModel.objects.active().filter(
            car=listing.car,
            price_usd__isnull=False,
        )

        return {
            'total_views': listing.total_views,
            'views_day': listing.views_day,
            'views_week': listing.views_week,
            'views_month': listing.views_month,
            'average_price_by_region': similar_by_region.aggregate(
                average=Avg('price_usd'),
            )['average'],
            'average_price_by_country': similar_by_country.aggregate(
                average=Avg('price_usd'),
            )['average'],
        }