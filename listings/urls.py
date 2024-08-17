from django.urls import path
from .views import ListingCreateView, PremiumStatsView, ListingUpdateView, \
    ListingDeleteView, ListingListView, ListingAddPhotoAPIView

urlpatterns = [
    path('create/', ListingCreateView.as_view(), name='listing-create'),
    path('update/<int:pk>/', ListingUpdateView.as_view(), name='listing_update'),
    path('delete/<int:pk>/', ListingDeleteView.as_view(), name='listing-delete'),
    path('premium/<int:listing_id>/stats/', PremiumStatsView.as_view(), name='premium_stats'),
    path('list/', ListingListView.as_view(), name='listing_list'),
    path('photo/<int:listing_id>/', ListingAddPhotoAPIView.as_view(), name='add__listing_photo'),
]

