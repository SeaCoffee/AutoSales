from rest_framework import serializers

from apps.cars.models import Brand, CarModel, ModelName
from apps.cars.serializers import CarSerializer
from apps.currency.models import CurrencyModel
from apps.listings.models import ListingModel
from apps.listings.services import ListingService, ListingServiceError
from core.enums.country_region_enum import Region
from core.validators.listings_validators import (
    get_required_request,
    validate_brand_request_data,
    validate_listing_photo_size,
)


class ListingPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingModel
        fields = ('listing_photo',)

    def validate_listing_photo(self, photo):
        return validate_listing_photo_size(photo)


class ListingCreateSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        write_only=True,
    )
    model_name = serializers.PrimaryKeyRelatedField(
        queryset=ModelName.objects.all(),
        write_only=True,
    )
    body_type = serializers.ChoiceField(
        choices=CarModel.BODY_TYPES,
        write_only=True,
    )
    currency = serializers.PrimaryKeyRelatedField(
        queryset=CurrencyModel.objects.all(),
    )
    region = serializers.ChoiceField(
        choices=Region.choices(),
    )
    listing_photo = serializers.ImageField(
        allow_null=True,
        required=False,
    )

    class Meta:
        model = ListingModel
        fields = (
            'id',
            'brand',
            'model_name',
            'body_type',
            'year',
            'engine',
            'title',
            'description',
            'listing_photo',
            'price',
            'currency',
            'region',
            'active',
            'initial_currency_rate',
            'price_usd',
            'price_eur',
            'price_uah',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'active',
            'initial_currency_rate',
            'price_usd',
            'price_eur',
            'price_uah',
            'created_at',
            'updated_at',
        )

    def validate_listing_photo(self, photo):
        return validate_listing_photo_size(photo)

    def create(self, validated_data):
        request = get_required_request(self)

        try:
            return ListingService.create_listing(
                data=validated_data,
                seller=request.user,
            )
        except ListingServiceError as error:
            raise serializers.ValidationError(error.as_dict()) from error


class ListingUpdateSerializer(serializers.ModelSerializer):
    currency = serializers.PrimaryKeyRelatedField(
        queryset=CurrencyModel.objects.all(),
        required=False,
    )
    region = serializers.ChoiceField(
        choices=Region.choices(),
        required=False,
    )
    listing_photo = serializers.ImageField(
        allow_null=True,
        required=False,
    )

    class Meta:
        model = ListingModel
        fields = (
            'title',
            'description',
            'listing_photo',
            'price',
            'currency',
            'region',
            'year',
            'engine',
        )

    def validate_listing_photo(self, photo):
        return validate_listing_photo_size(photo)

    def update(self, instance, validated_data):
        old_photo = instance.listing_photo

        try:
            listing = ListingService.update_listing(
                listing=instance,
                data=validated_data,
            )
        except ListingServiceError as error:
            raise serializers.ValidationError(error.as_dict()) from error

        new_photo = validated_data.get('listing_photo')

        if new_photo and old_photo and old_photo != listing.listing_photo:
            old_photo.delete(save=False)

        return listing


class ListingListSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    currency_code = serializers.CharField(source='currency.currency_code', read_only=True)

    class Meta:
        model = ListingModel
        fields = (
            'id',
            'title',
            'description',
            'listing_photo',
            'active',
            'price',
            'currency',
            'currency_code',
            'price_usd',
            'price_eur',
            'price_uah',
            'region',
            'year',
            'engine',
            'car',
            'created_at',
        )


class ListingDetailSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    currency_code = serializers.CharField(source='currency.currency_code', read_only=True)
    current_currency_rate = serializers.SerializerMethodField()
    total_views = serializers.IntegerField(read_only=True)

    class Meta:
        model = ListingModel
        fields = (
            'id',
            'car',
            'seller',
            'seller_username',
            'title',
            'description',
            'listing_photo',
            'active',
            'views_day',
            'views_week',
            'views_month',
            'total_views',
            'edit_attempts',
            'price',
            'currency',
            'currency_code',
            'price_usd',
            'price_eur',
            'price_uah',
            'initial_currency_rate',
            'current_currency_rate',
            'region',
            'year',
            'engine',
            'created_at',
            'updated_at',
        )
        read_only_fields = fields

    def get_current_currency_rate(self, obj):
        return ListingService.get_current_rate(obj.currency)


class PremiumStatsSerializer(serializers.Serializer):
    total_views = serializers.IntegerField()
    views_day = serializers.IntegerField()
    views_week = serializers.IntegerField()
    views_month = serializers.IntegerField()
    average_price_by_region = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        allow_null=True,
    )
    average_price_by_country = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        allow_null=True,
    )


class BrandRequestSerializer(serializers.Serializer):
    brand_name = serializers.CharField(max_length=100)
    model_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):
        return validate_brand_request_data(
            brand_name=attrs.get('brand_name'),
            model_name=attrs.get('model_name'),
        )