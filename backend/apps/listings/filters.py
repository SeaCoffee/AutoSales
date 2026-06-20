import django_filters

from apps.cars.models import Brand, CarModel, ModelName
from core.enums.country_region_enum import Region

from apps.listings.models import ListingModel


class ListingFilter(django_filters.FilterSet):
    brand = django_filters.ModelChoiceFilter(
        field_name='car__brand',
        queryset=Brand.objects.all(),
    )
    model_name = django_filters.ModelChoiceFilter(
        field_name='car__model_name',
        queryset=ModelName.objects.all(),
    )
    body_type = django_filters.ChoiceFilter(
        field_name='car__body_type',
        choices=CarModel.BODY_TYPES,
    )
    min_year = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='gte',
    )
    max_year = django_filters.NumberFilter(
        field_name='year',
        lookup_expr='lte',
    )
    region = django_filters.ChoiceFilter(
        field_name='region',
        choices=Region.choices(),
    )
    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
    )
    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
    )
    active = django_filters.BooleanFilter(
        field_name='active',
    )

    class Meta:
        model = ListingModel
        fields = (
            'brand',
            'model_name',
            'body_type',
            'min_year',
            'max_year',
            'region',
            'price_min',
            'price_max',
            'active',
        )