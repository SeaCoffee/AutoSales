import django_filters
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.listings.filters import ListingFilter
from apps.listings.models import ListingModel
from apps.listings.serializers import (
    BrandRequestSerializer,
    ListingCreateSerializer,
    ListingDetailSerializer,
    ListingListSerializer,
    ListingPhotoSerializer,
    ListingUpdateSerializer,
    PremiumStatsSerializer,
)
from apps.listings.services import ListingService
from core.enums.country_region_enum import Region
from core.pagination import PagePagination
from core.permissions import (
    IsPremiumSeller,
    IsSeller,
    IsSellerOrManagerAndOwner,
    get_user_role_name,
)


class ListingCreateView(CreateAPIView):
    queryset = ListingModel.objects.all()
    serializer_class = ListingCreateSerializer
    permission_classes = (IsSeller,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)


class ListingPhotoUpdateAPIView(UpdateAPIView):
    serializer_class = ListingPhotoSerializer
    permission_classes = (IsSellerOrManagerAndOwner,)
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return ListingModel.objects.with_related()


class ListingUpdateView(UpdateAPIView):
    serializer_class = ListingUpdateSerializer
    permission_classes = (IsSellerOrManagerAndOwner,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        user = self.request.user
        role_name = get_user_role_name(user)

        queryset = ListingModel.objects.with_related()

        if role_name == 'seller':
            return queryset.for_seller(user)

        return queryset


class ListingDeleteView(DestroyAPIView):
    serializer_class = ListingDetailSerializer
    permission_classes = (IsSellerOrManagerAndOwner,)

    def get_queryset(self):
        user = self.request.user
        role_name = get_user_role_name(user)

        queryset = ListingModel.objects.with_related()

        if role_name == 'seller':
            return queryset.for_seller(user)

        return queryset


class ListingListView(ListAPIView):
    serializer_class = ListingListSerializer
    permission_classes = (AllowAny,)
    pagination_class = PagePagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = ListingFilter

    def get_queryset(self):
        return ListingModel.objects.with_related().active()


class UserListingsView(ListAPIView):
    serializer_class = ListingListSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PagePagination

    def get_queryset(self):
        return (
            ListingModel.objects
            .with_related()
            .for_seller(self.request.user)
        )


class ListingPublicDetailView(RetrieveAPIView):
    serializer_class = ListingDetailSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return ListingModel.objects.with_related().active()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ListingService.increment_public_view(instance)

        serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ListingOwnerDetailView(RetrieveAPIView):
    serializer_class = ListingDetailSerializer
    permission_classes = (IsSellerOrManagerAndOwner,)

    def get_queryset(self):
        user = self.request.user
        role_name = get_user_role_name(user)

        queryset = ListingModel.objects.with_related()

        if role_name == 'seller':
            return queryset.for_seller(user)

        return queryset


class PremiumStatsView(RetrieveAPIView):
    serializer_class = PremiumStatsSerializer
    permission_classes = (IsAuthenticated, IsPremiumSeller)

    def get(self, request, *args, **kwargs):
        listing = get_object_or_404(
            ListingModel.objects.with_related(),
            id=kwargs.get('listing_id'),
            seller=request.user,
        )

        serializer = self.get_serializer(
            ListingService.get_premium_stats(listing),
        )

        return Response(serializer.data)


class RegionsAPIView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response(
            {
                'regions': [
                    {
                        'value': region.value,
                        'label': region.name,
                    }
                    for region in Region
                ],
            }
        )


class BrandRequestView(GenericAPIView):
    serializer_class = BrandRequestSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ListingService.send_brand_request(
            brand_name=serializer.validated_data['brand_name'],
            model_name=serializer.validated_data.get('model_name') or None,
            username=request.user.username,
        )

        return Response(
            {'detail': 'Brand request has been sent to managers.'},
            status=status.HTTP_201_CREATED,
        )