from django.core.exceptions import ValidationError
from django.conf import settings


def image_size(value):
    if value.size > settings.SIZE_IMAGE:
        raise ValidationError('Картинки размером больше 1Mb не поддерживаются')
    return value
