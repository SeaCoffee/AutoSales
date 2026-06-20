from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users_auth.models import UserRoleModel
from core.validators.users_validators import (
    normalize_email,
    validate_password_strength,
)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return normalize_email(value)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_password(self, value):
        return validate_password_strength(value)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['account_type'] = user.account_type

        role = getattr(user, 'role', None)
        if role:
            token['role'] = role.name

        return token


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleModel
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')