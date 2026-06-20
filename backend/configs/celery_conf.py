import os

from celery.schedules import crontab


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'django-db')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE', 'UTC')
CELERY_ENABLE_UTC = True

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_IMPORTS = (
    'core.services.email_service',
    'apps.currency.services',
)

CELERY_BEAT_SCHEDULE = {
    'update-currency-rates-midnight': {
        'task': 'apps.currency.services.update_currency_rates',
        'schedule': crontab(hour=0, minute=1),
    },
    'retry-update-currency-rates-noon': {
        'task': 'apps.currency.services.update_currency_rates',
        'schedule': crontab(hour=12, minute=0),
    },
}