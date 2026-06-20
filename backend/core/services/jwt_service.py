from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import BlacklistMixin, Token

from core.enums.tokens_enum import ActionTokenEnum


class CustomToken(Token):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        token['account_type'] = user.account_type

        role = getattr(user, 'role', None)
        if role:
            token['role'] = role.name

        return token


class ActivateToken(BlacklistMixin, CustomToken):
    token_type = ActionTokenEnum.ACTIVATE.token_type
    lifetime = ActionTokenEnum.ACTIVATE.lifetime


class RecoveryToken(BlacklistMixin, CustomToken):
    token_type = ActionTokenEnum.RECOVERY.token_type
    lifetime = ActionTokenEnum.RECOVERY.lifetime


class AccessToken(BlacklistMixin, CustomToken):
    token_type = ActionTokenEnum.ACCESS.token_type
    lifetime = ActionTokenEnum.ACCESS.lifetime


class SocketToken(CustomToken):
    token_type = ActionTokenEnum.SOCKET.token_type
    lifetime = ActionTokenEnum.SOCKET.lifetime


class JWTService:
    @staticmethod
    def create_token(user, token_class=ActivateToken):
        token = token_class.for_user(user)
        token['created_by'] = token_class.__name__

        return token

    @staticmethod
    def get_user_from_token_payload(token_obj):
        user_id = token_obj.payload.get('user_id')

        if user_id is None:
            raise ValueError('Invalid token payload.')

        UserModel = get_user_model()

        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist as error:
            raise ValueError('User not found.') from error

    @classmethod
    def validate_socket_token(cls, token):
        try:
            token_obj = SocketToken(token)
            return cls.get_user_from_token_payload(token_obj)
        except Exception as error:
            raise ValueError('Invalid or expired socket token.') from error

    @classmethod
    def validate_token(cls, token, token_class):
        try:
            token_obj = token_class(token)
            token_obj.check_blacklist()

            user = cls.get_user_from_token_payload(token_obj)
            token_obj.blacklist()

            return user
        except Exception as error:
            raise ValueError('Invalid or expired token.') from error

    @staticmethod
    def update_user_account_type(user, new_type):
        user.account_type = new_type
        user.save(update_fields=('account_type', 'updated_at'))

        return JWTService.create_token(user, AccessToken)