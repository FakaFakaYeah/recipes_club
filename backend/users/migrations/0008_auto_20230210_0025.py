# Generated by Django 2.2.16 on 2023-02-09 21:25

import django.core.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20230210_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'Данное имя пользователя уже занято!'}, help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Zа-яА-Я0-9@/./+/-/_]+$'), users.validators.validate_username], verbose_name='Имя пользователя'),
        ),
    ]
