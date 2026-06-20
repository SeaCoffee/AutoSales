from django.db import models
from django.core.exceptions import ValidationError

from core.models import BaseModel


class Brand(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'brand'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ModelName(BaseModel):
    brand = models.ForeignKey(
        Brand,
        related_name='models',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'model_name'
        ordering = ('brand__name', 'name')
        constraints = [
            models.UniqueConstraint(
                fields=('brand', 'name'),
                name='unique_model_name_per_brand',
            ),
        ]

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class CarModel(BaseModel):
    BODY_TYPES = [
        ('sedan', 'Sedan'),
        ('hatchback', 'Hatchback'),
        ('suv', 'SUV'),
        ('wagon', 'Wagon'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('minivan', 'Minivan'),
        ('pickup', 'Pickup'),
    ]

    brand = models.ForeignKey(
        Brand,
        related_name='cars',
        on_delete=models.CASCADE,
    )
    model_name = models.ForeignKey(
        ModelName,
        related_name='cars',
        on_delete=models.CASCADE,
    )
    body_type = models.CharField(
        max_length=50,
        choices=BODY_TYPES,
    )

    class Meta:
        db_table = 'cars'
        ordering = ('brand__name', 'model_name__name', 'body_type')
        constraints = [
            models.UniqueConstraint(
                fields=('brand', 'model_name', 'body_type'),
                name='unique_car_configuration',
            ),
        ]

    def __str__(self):
        return f'{self.brand.name} {self.model_name.name} ({self.body_type})'

    def clean(self):
        super().clean()

        if self.model_name and self.brand and self.model_name.brand_id != self.brand_id:


            raise ValidationError(
                {
                    'model_name': 'Selected model does not belong to selected brand.',
                }
            )