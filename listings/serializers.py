from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import ListingModel
from cars.models import CarModel
from users.models import UserModel
from core.enums.profanity_enum import ProfanityFilter
from core.services.email_service import EmailService
from cars.serializers import CarSerializer
from core.services.managers_notification import ManagerNotificationService
from currency.models import CurrencyModel
from cars.serializers import CarSerializer, Brand, ModelName
from core.enums.country_region_enum import Region
from django.contrib.auth import get_user_model



class ListingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingModel
        fields = ['listing_photo']

    def validate_listings_photo(self, photo):
        max_size = 100 * 1024
        if photo.size > max_size:
            raise ValidationError('Maximum size of 100KB exceeded')
        return photo

class ListingCreateSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), write_only=True)
    model_name = serializers.PrimaryKeyRelatedField(queryset=ModelName.objects.all(), write_only=True)
    body_type = serializers.ChoiceField(choices=CarModel.BODY_TYPES, write_only=True)
    currency = serializers.PrimaryKeyRelatedField(queryset=CurrencyModel.objects.all())
    region = serializers.ChoiceField(choices=Region.choices())

    class Meta:
        model = ListingModel
        fields = (
            'brand', 'model_name', 'body_type', 'year', 'engine', 'title', 'description', 'listing_photo', 'price',
            'currency', 'region'
        )

    def validate_description(self, value):
        instance = self.instance
        if ProfanityFilter.is_profane(value):
            if instance:
                instance.edit_attempts += 1
                instance.save()
                if instance.edit_attempts >= 3:
                    instance.active = False
                    instance.save()
                    seller = instance.seller
                    managers = get_user_model().objects.filter(role_id=3)
                    for manager in managers:
                        ManagerNotificationService.send_profanity_notification(
                            description=value,
                            username=seller.username,
                            manager=manager
                        )
                    raise serializers.ValidationError("Maximum edit attempts exceeded. The listing has been deactivated.")
                raise serializers.ValidationError("The description contains prohibited words.")
        return value

    def validate(self, data):
        request = self.context.get('request')
        seller = request.user

        # Проверка на тип аккаунта
        if seller.account_type == 'basic' and ListingModel.objects.filter(seller=seller).count() >= 1:
            raise serializers.ValidationError("Basic account holders can only create one listing.")

        brand = data.get('brand')
        model_name = data.get('model_name')

        # Проверка существования модели под брендом
        if not ModelName.objects.filter(brand=brand, id=model_name.id).exists():
            ManagerNotificationService.send_notification(
                brand_name=str(brand),
                model_name=str(model_name),
                username=seller.username
            )
            raise serializers.ValidationError("Car model with specified details does not exist. You can request to add a new brand.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        seller = request.user

        # Вызываем метод create_listing из менеджера модели
        return ListingModel.objects.create_listing(validated_data, seller)


class ListingDetailSerializer(serializers.ModelSerializer):
    # Использование методов для получения brand, model_name и body_type
    brand = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()
    body_type = serializers.SerializerMethodField()

    class Meta:
        model = ListingModel
        fields = (
            'id', 'brand', 'model_name', 'body_type', 'year', 'engine', 'title', 'description', 'listing_photo', 'price',
            'currency', 'region', 'seller'
        )

    def get_brand(self, obj):
        return obj.car.brand.id

    def get_model_name(self, obj):
        return obj.car.model_name.id

    def get_body_type(self, obj):
        return obj.car.body_type

class ListingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingModel
        fields = ('description', 'listing_photo', 'price', 'currency')

    def validate_description(self, value):
        instance = self.instance
        if ProfanityFilter.is_profane(value):
            instance.edit_attempts += 1
            instance.save()
            if instance.edit_attempts >= 3:
                instance.active = False
                instance.save()

                seller = instance.seller
                managers = get_user_model().objects.filter(role_id=3)
                for manager in managers:
                    ManagerNotificationService.send_profanity_notification(
                        description=value,
                        username=seller.username,
                        manager=manager
                    )
                raise serializers.ValidationError("Maximum edit attempts exceeded. The listing has been deactivated.")
            raise serializers.ValidationError("The description contains prohibited words.")
        return value

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.active = True
        instance.save()
        return instance


class PremiumStatsSerializer(serializers.Serializer):
    total_views = serializers.IntegerField()
    views_day = serializers.IntegerField()
    views_week = serializers.IntegerField()
    views_month = serializers.IntegerField()
    average_price_by_region = serializers.FloatField(allow_null=True)
    average_price_by_country = serializers.FloatField(allow_null=True)

class ListingListSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)

    class Meta:
        model = ListingModel
        fields = ['title', 'description', 'listing_photo', 'active', 'car']
