from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидатор проверки запрещенных
    username при регистрации пользователя"""
    if value.lower() in ('me', 'user', 'admin', 'administrator'):
        raise ValidationError('Нельзя создавать пользователя с таким именем')
