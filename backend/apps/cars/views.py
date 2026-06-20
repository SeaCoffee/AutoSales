from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny

from apps.cars.filters import CarFilter
from apps.cars.models import Brand, CarModel, ModelName
from apps.cars.serializers import (
    BrandSerializer,
    BrandWithModelsSerializer,
    CarListSerializer,
    CarSerializer,
    ModelNameSerializer,
)
from core.pagination import PagePagination
from core.permissions import IsManager


class CarListCreateView(ListCreateAPIView):
    pagination_class = PagePagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = CarFilter
    search_fields = (
        'brand__name',
        'model_name__name',
        'body_type',
    )
    ordering_fields = (
        'brand__name',
        'model_name__name',
        'body_type',
        'created_at',
    )
    ordering = (
        'brand__name',
        'model_name__name',
    )

    def get_queryset(self):
        return CarModel.objects.select_related(
            'brand',
            'model_name',
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CarListSerializer

        return CarSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)

        return (IsManager(),)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        return CarModel.objects.select_related(
            'brand',
            'model_name',
        )

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)

        return (IsManager(),)


class BrandListCreateView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = (
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ('name',)
    ordering_fields = ('name', 'created_at')
    ordering = ('name',)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)

        return (IsManager(),)


class BrandRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)

        return (IsManager(),)


class ModelNameListCreateView(ListCreateAPIView):
    serializer_class = ModelNameSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = ('brand',)
    search_fields = ('name', 'brand__name')
    ordering_fields = ('name', 'brand__name', 'created_at')
    ordering = ('brand__name', 'name')

    def get_queryset(self):
        return ModelName.objects.select_related('brand')

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)

        return (IsManager(),)


class ModelNameRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ModelNameSerializer

    def get_queryset(self):
        return ModelName.objects.select_related('brand')

    def get_permissions(self):
        if self.request.method == 'GET':
            return (AllowAny(),)

        return (IsManager(),)


class BrandModelDataView(ListAPIView):
    queryset = Brand.objects.prefetch_related('models')
    serializer_class = BrandWithModelsSerializer
    permission_classes = (AllowAny,)