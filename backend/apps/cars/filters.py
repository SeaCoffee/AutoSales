import django_filters

from apps.cars.models import Brand, CarModel, ModelName


class CarFilter(django_filters.FilterSet):
    brand = django_filters.ModelChoiceFilter(
        field_name='brand',
        queryset=Brand.objects.all(),
    )
    model_name = django_filters.ModelChoiceFilter(
        field_name='model_name',
        queryset=ModelName.objects.all(),
    )
    body_type = django_filters.ChoiceFilter(
        field_name='body_type',
        choices=CarModel.BODY_TYPES,
    )

    class Meta:
        model = CarModel
        fields = (
            'brand',
            'model_name',
            'body_type',
        )