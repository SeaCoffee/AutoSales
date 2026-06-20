from django.urls import path

from apps.listings.views import (
    BrandRequestView,
    ListingCreateView,
    ListingDeleteView,
    ListingListView,
    ListingOwnerDetailView,
    ListingPhotoUpdateAPIView,
    ListingPublicDetailView,
    ListingUpdateView,
    PremiumStatsView,
    RegionsAPIView,
    UserListingsView,
)


urlpatterns = [
    path('', ListingListView.as_view(), name='listing-list'),
    path('create/', ListingCreateView.as_view(), name='listing-create'),
    path('regions/', RegionsAPIView.as_view(), name='listing-regions'),
    path('me/', UserListingsView.as_view(), name='user-listings'),

    path('<int:pk>/', ListingPublicDetailView.as_view(), name='listing-detail'),
    path('<int:pk>/owner/', ListingOwnerDetailView.as_view(), name='listing-owner-detail'),
    path('<int:pk>/update/', ListingUpdateView.as_view(), name='listing-update'),
    path('<int:pk>/delete/', ListingDeleteView.as_view(), name='listing-delete'),
    path('<int:pk>/photo/', ListingPhotoUpdateAPIView.as_view(), name='listing-photo-update'),

    path('<int:listing_id>/premium/stats/', PremiumStatsView.as_view(), name='premium-stats'),
    path('brands/request/', BrandRequestView.as_view(), name='brand-request'),
]