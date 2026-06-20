from rest_framework import serializers

from apps.cars.models import Brand, CarModel, ModelName
from core.validators.cars_validators import (
    normalize_dictionary_name,
    validate_model_name_belongs_to_brand,
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
        )

    def validate_name(self, value):
        return normalize_dictionary_name(value)


class ModelNameSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = ModelName
        fields = (
            'id',
            'brand',
            'brand_name',
            'name',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'brand_name',
            'created_at',
            'updated_at',
        )

    def validate_name(self, value):
        return normalize_dictionary_name(value)


class CarSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    model_name_value = serializers.CharField(source='model_name.name', read_only=True)

    class Meta:
        model = CarModel
        fields = (
            'id',
            'brand',
            'brand_name',
            'model_name',
            'model_name_value',
            'body_type',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'brand_name',
            'model_name_value',
            'created_at',
            'updated_at',
        )

    def validate(self, attrs):
        brand = attrs.get('brand') or getattr(self.instance, 'brand', None)
        model_name = attrs.get('model_name') or getattr(self.instance, 'model_name', None)

        validate_model_name_belongs_to_brand(
            brand=brand,
            model_name=model_name,
        )

        return attrs


class CarListSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.name', read_only=True)
    model_name = serializers.CharField(source='model_name.name', read_only=True)

    class Meta:
        model = CarModel
        fields = (
            'id',
            'brand',
            'model_name',
            'body_type',
        )


class BrandWithModelsSerializer(serializers.ModelSerializer):
    models = ModelNameSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = (
            'id',
            'name',
            'models',
        )