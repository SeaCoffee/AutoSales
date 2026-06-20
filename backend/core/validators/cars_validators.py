from rest_framework.exceptions import ValidationError


def normalize_dictionary_name(value: str) -> str:
    normalized = str(value).strip()

    if not normalized:
        raise ValidationError('Name cannot be empty.')

    return normalized


def validate_model_name_belongs_to_brand(*, brand, model_name) -> None:
    if not brand or not model_name:
        return

    if model_name.brand_id != brand.id:
        raise ValidationError(
            {
                'model_name': 'Selected model does not belong to selected brand.',
            }
        )