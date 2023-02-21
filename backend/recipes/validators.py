from django.core.exceptions import ValidationError


def image_size(value):
    if value.size > 1 * 1024 * 1024:
        raise ValidationError('Слишком большое фото!')
    return value
