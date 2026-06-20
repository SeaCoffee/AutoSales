from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.currency.models import CurrencyModel
from apps.currency.serializers import CurrencySerializer


class CurrencyListAPIView(ListAPIView):
    queryset = CurrencyModel.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (AllowAny,)