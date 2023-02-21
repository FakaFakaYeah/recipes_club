from django.core.exceptions import ValidationError

from foodgram.settings import SIZE_IMAGE


def image_size(value):
    if value.size > SIZE_IMAGE:
        raise ValidationError('Картинки размером больше 1Mb не поддерживаются')
    return value
