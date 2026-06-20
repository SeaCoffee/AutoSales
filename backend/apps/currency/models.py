from django.db import models

from core.models import BaseModel


class CurrencyModel(BaseModel):
    currency_code = models.CharField(max_length=3, unique=True)
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        db_table = 'currency'
        ordering = ('currency_code',)
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rate__gt=0),
                name='currency_rate_positive',
            ),
        ]

    def __str__(self):
        return f'{self.currency_code}: {self.rate}'