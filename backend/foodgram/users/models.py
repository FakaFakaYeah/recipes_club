from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q, F

from .validators import validate_username


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Обязательное поле. Не более 150 символов. '
                  'Только буквы, цифры и символы @/./+/-/_.',
        error_messages={'unique': 'Данное имя пользователя уже занято!'},
        validators=[UnicodeUsernameValidator, validate_username],
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='пароль'
    )

    class Meta:
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
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
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки'
    )

    class Meta:
        verbose_name_plural = 'Подписки'
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(fields=['user', 'author'], name='unique_follow'),
            CheckConstraint(check=~Q(user=F('author')),
                            name='subscribe_to_yourself')
        ]

    def __str__(self):
        return f'{self.user} --> {self.author}'
