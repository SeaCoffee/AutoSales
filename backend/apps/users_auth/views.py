from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users_auth.models import UserRoleModel
from apps.users_auth.serializers import (
    CustomTokenObtainPairSerializer,
    EmailSerializer,
    ResetPasswordSerializer,
    UserRoleSerializer,
)
from core.services.email_service import EmailService
from core.services.jwt_service import (
    ActivateToken,
    JWTService,
    RecoveryToken,
    SocketToken,
)


UserModel = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserActivateAPIView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, token, *args, **kwargs):
        try:
            user = JWTService.validate_token(token, ActivateToken)
        except ValueError as error:
            return Response(
                {'detail': str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=('is_active', 'updated_at'))

        return Response(
            {'detail': 'Account activated successfully.'},
            status=status.HTTP_200_OK,
        )


class UserRecoverAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = UserModel.objects.filter(email=email).first()

        if user:
            EmailService.recovery_password(user)

        return Response(
            {
                'detail': (
                    'If an account with this email exists, '
                    'recovery instructions have been sent.'
                ),
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = JWTService.validate_token(token, RecoveryToken)
        except ValueError as error:
            return Response(
                {'detail': str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['password'])
        user.save(update_fields=('password', 'updated_at'))

        return Response(
            {'detail': 'Password has been changed.'},
            status=status.HTTP_200_OK,
        )


class RoleListAPIView(ListAPIView):
    queryset = UserRoleModel.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = (AllowAny,)


class SocketTokenAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = JWTService.create_token(request.user, SocketToken)

        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK,
        )