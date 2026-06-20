from decimal import Decimal, InvalidOperation

import requests
from celery import shared_task
from django.db import transaction

from apps.currency.models import CurrencyModel


PRIVATBANK_API_URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
TARGET_CURRENCIES = {'USD', 'EUR'}
BASE_CURRENCY = 'UAH'


class CurrencyRateUpdateError(Exception):
    pass


def parse_rate(value) -> Decimal:
    try:
        rate = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise CurrencyRateUpdateError('Invalid currency rate value.') from error

    if rate <= Decimal('0'):
        raise CurrencyRateUpdateError('Currency rate must be greater than zero.')

    return rate


def fetch_privatbank_rates() -> list[dict]:
    response = requests.get(PRIVATBANK_API_URL, timeout=10)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise CurrencyRateUpdateError('Unexpected PrivatBank response format.')

    return data


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=3600,
    name='apps.currency.services.currency_service.update_currency_rates',
)
def update_currency_rates(self):
    try:
        rates = fetch_privatbank_rates()

        with transaction.atomic():
            CurrencyModel.objects.update_or_create(
                currency_code=BASE_CURRENCY,
                defaults={
                    'rate': Decimal('1.0000'),
                },
            )

            for item in rates:
                currency_code = item.get('ccy')

                if currency_code not in TARGET_CURRENCIES:
                    continue

                rate = parse_rate(item.get('sale'))

                CurrencyModel.objects.update_or_create(
                    currency_code=currency_code,
                    defaults={
                        'rate': rate,
                    },
                )

    except Exception as error:
        raise self.retry(exc=error) from error