from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q, F

from .validators import validate_username


class User(AbstractUser):
    """Собственная модель пользователей"""
    email = models.EmailField(
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True
    )
    username = models.CharField(
        max_length=settings.FIELD_LENGTH_USER,
        unique=True,
        help_text='Обязательное поле. Не более 150 символов. '
                  'Только буквы, цифры и символы @/./+/-/_.',
        error_messages={'unique': 'Данное имя пользователя уже занято!'},
        validators=[UnicodeUsernameValidator, validate_username],
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=settings.FIELD_LENGTH_USER,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=settings.FIELD_LENGTH_USER,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=settings.FIELD_LENGTH_USER,
        verbose_name='пароль'
    )
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок на пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='На кого подписывается'
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        constraints = [
            UniqueConstraint(fields=['user', 'author'], name='unique_follow'),
            CheckConstraint(check=~Q(user=F('author')),
                            name='subscribe_to_yourself')
        ]

    def __str__(self):
        return f'{self.user.username} --> {self.author.username}'
