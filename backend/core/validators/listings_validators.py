from rest_framework.exceptions import ValidationError


def validate_listing_photo_size(photo, *, max_size_mb: int = 2):
    max_size = max_size_mb * 1024 * 1024

    if photo.size > max_size:
        raise ValidationError(f'Photo size must not exceed {max_size_mb} MB.')

    return photo


def get_required_request(serializer):
    request = serializer.context.get('request')

    if not request:
        raise ValidationError({'detail': 'Request context is required.'})

    return request


def normalize_optional_name(value: str | None) -> str:
    return str(value or '').strip()


def validate_required_name(value: str, field_name: str = 'name') -> str:
    normalized = normalize_optional_name(value)

    if not normalized:
        raise ValidationError({field_name: 'This field cannot be empty.'})

    return normalized


def validate_brand_request_data(*, brand_name: str, model_name: str | None = None) -> dict:
    return {
        'brand_name': validate_required_name(brand_name, 'brand_name'),
        'model_name': normalize_optional_name(model_name),
    }