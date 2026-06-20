from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError


UserModel = get_user_model()


def normalize_email(value: str) -> str:
    return str(value).strip().lower()


def validate_password_strength(value: str, user=None) -> str:
    try:
        django_validate_password(value, user=user)
    except DjangoValidationError as error:
        raise ValidationError(list(error.messages)) from error

    return value


def validate_avatar_file_size(file, *, max_size_mb: int = 2):
    max_size = max_size_mb * 1024 * 1024

    if file.size > max_size:
        raise ValidationError(f'Avatar size must not exceed {max_size_mb} MB.')

    return file


def get_existing_user_by_id(user_id: int):
    user = UserModel.objects.filter(id=user_id).first()

    if not user:
        raise ValidationError('User not found.')

    return user


def validate_user_is_not_self(*, request_user, target_user_id: int) -> None:
    if request_user and request_user.is_authenticated and request_user.id == target_user_id:
        raise ValidationError('You cannot add yourself to blacklist.')


def validate_blacklist_target(*, target_user_id: int, request_user=None):
    validate_user_is_not_self(
        request_user=request_user,
        target_user_id=target_user_id,
    )

    return get_existing_user_by_id(target_user_id)