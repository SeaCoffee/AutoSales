from datetime import date
from decimal import Decimal

from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models import F

from apps.cars.models import CarModel
from core.enums.country_region_enum import Region
from core.models import BaseModel
from core.services.upload_photos import upload_photo_listing
from apps.currency.models import CurrencyModel

from apps.listings.manager import ListingManager


class ListingModel(BaseModel):
    car = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name='listings',
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    listing_photo = models.ImageField(
        upload_to=upload_photo_listing,
        blank=True,
        null=True,
        validators=[
            validators.FileExtensionValidator(['jpeg', 'jpg', 'png', 'webp']),
        ],
    )
    active = models.BooleanField(default=False)

    views_day = models.PositiveIntegerField(default=0)
    views_week = models.PositiveIntegerField(default=0)
    views_month = models.PositiveIntegerField(default=0)
    edit_attempts = models.PositiveSmallIntegerField(default=0)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(Decimal('0.01')),
        ],
    )
    currency = models.ForeignKey(
        CurrencyModel,
        on_delete=models.PROTECT,
        related_name='listings',
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
    )
    price_eur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
    )
    price_uah = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
    )
    initial_currency_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        editable=False,
    )

    region = models.CharField(
        max_length=50,
        choices=Region.choices(),
        default=Region.KYIV.value,
    )
    year = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(1900),
            validators.MaxValueValidator(date.today().year + 1),
        ],
    )
    engine = models.CharField(max_length=255)

    objects = ListingManager()

    class Meta:
        db_table = 'listings'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    @property
    def total_views(self):
        return self.views_day + self.views_week + self.views_month

    def increment_views(self):
        type(self).objects.filter(pk=self.pk).update(
            views_day=F('views_day') + 1,
            views_week=F('views_week') + 1,
            views_month=F('views_month') + 1,
        )
        self.refresh_from_db(
            fields=[
                'views_day',
                'views_week',
                'views_month',
            ],
        )