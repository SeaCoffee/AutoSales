from django.urls import path

from .views import (
    BrandListCreateView,
    BrandModelDataView,
    BrandRetrieveUpdateDestroyView,
    CarListCreateView,
    CarRetrieveUpdateDestroyView,
    ModelNameListCreateView,
    ModelNameRetrieveUpdateDestroyView,
)


urlpatterns = [
    path('', CarListCreateView.as_view(), name='car-list-create'),
    path('<int:pk>/', CarRetrieveUpdateDestroyView.as_view(), name='car-detail'),

    path('brands/', BrandListCreateView.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', BrandRetrieveUpdateDestroyView.as_view(), name='brand-detail'),

    path('models/', ModelNameListCreateView.as_view(), name='model-name-list-create'),
    path('models/<int:pk>/', ModelNameRetrieveUpdateDestroyView.as_view(), name='model-name-detail'),

    path('data/', BrandModelDataView.as_view(), name='brand-model-data'),
]