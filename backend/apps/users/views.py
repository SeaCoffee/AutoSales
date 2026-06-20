from django.http import Http404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import ProfileModel
from apps.users.serializers import (
    AddToBlacklistSerializer,
    BlacklistSerializer,
    CurrentUserSerializer,
    ManagerCreateSerializer,
    ProfileAvatarSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
)
from apps.users.services import (
    BlacklistService,
    UserAccountService,
    UsersServiceError,
)
from core.permissions import IsManager


class UserCreateAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class CurrentUserDetailsView(RetrieveAPIView):
    serializer_class = CurrentUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileDetailView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.user.profile
        except ProfileModel.DoesNotExist as error:
            raise Http404('Profile not found.') from error


class ProfileUpdateView(UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.user.profile
        except ProfileModel.DoesNotExist as error:
            raise Http404('Profile not found.') from error


class PremiumRequestAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        UserAccountService.submit_premium_request(request.user)

        return Response(
            {'detail': 'Premium request has been submitted.'},
            status=status.HTTP_200_OK,
        )


class CreateManagerView(CreateAPIView):
    serializer_class = ManagerCreateSerializer
    permission_classes = (IsAdminUser,)


class UserAvatarUpdateAPIView(UpdateAPIView):
    serializer_class = ProfileAvatarSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        try:
            return self.request.user.profile
        except ProfileModel.DoesNotExist as error:
            raise Http404('Profile not found.') from error


class UserDeleteSelfView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        try:
            UserAccountService.delete_own_user(request.user)
        except UsersServiceError as error:
            return Response(
                error.as_dict(),
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class BlacklistManageView(GenericAPIView):
    permission_classes = (IsAuthenticated, IsManager)
    serializer_class = AddToBlacklistSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            blacklist_entry = BlacklistService.add_user(
                user=serializer.validated_data['user'],
                added_by=request.user,
                reason=serializer.validated_data.get('reason', ''),
            )
        except UsersServiceError as error:
            return Response(
                error.as_dict(),
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = BlacklistSerializer(blacklist_entry)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            BlacklistService.remove_user(
                user=serializer.validated_data['user'],
            )
        except UsersServiceError as error:
            return Response(
                error.as_dict(),
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)