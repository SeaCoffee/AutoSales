from django.urls import path

from apps.currency.views import CurrencyListAPIView


urlpatterns = [
    path('', CurrencyListAPIView.as_view(), name='currency-list'),
]