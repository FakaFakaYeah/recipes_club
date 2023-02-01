from django.core.exceptions import ValidationError


def validate_username(value):
    if str.lower(value) == 'me':
        raise ValidationError('Нельзя создавать пользователя с таким именем')
