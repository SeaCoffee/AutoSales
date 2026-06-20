from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from apps.users.models import BlacklistModel


UserModel = get_user_model()


class UsersServiceError(Exception):
    def __init__(self, message: str, field: str | None = None):
        self.message = message
        self.field = field
        super().__init__(message)

    def as_dict(self):
        if self.field:
            return {self.field: self.message}

        return {'detail': self.message}


class UserAccountService:
    @staticmethod
    def submit_premium_request(user):
        user.is_upgrade_to_premium = True
        user.save(update_fields=('is_upgrade_to_premium', 'updated_at'))

        return user

    @staticmethod
    @atomic
    def delete_own_user(user) -> None:
        if not user or not UserModel.objects.filter(id=user.id).exists():
            raise UsersServiceError('User with given ID does not exist.')

        user.delete()


class BlacklistService:
    @staticmethod
    @atomic
    def add_user(*, user, added_by, reason: str = ''):
        blacklist_entry, created = BlacklistModel.objects.get_or_create(
            user=user,
            defaults={
                'added_by': added_by,
                'reason': reason,
            },
        )

        if not created:
            raise UsersServiceError('User is already in blacklist.')

        return blacklist_entry

    @staticmethod
    @atomic
    def remove_user(*, user) -> None:
        deleted_count, _ = BlacklistModel.objects.filter(user=user).delete()

        if not deleted_count:
            raise UsersServiceError('User not found in blacklist.')