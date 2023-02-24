from django.core.exceptions import ValidationError
from django.conf import settings


def image_size(value):
    if value.size > settings.MAX_SIZE_IMAGE:
        raise ValidationError('Слишком большое фото!')
    return value
