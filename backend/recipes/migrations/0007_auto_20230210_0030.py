# Generated by Django 2.2.16 on 2023-02-09 21:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20230209_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(regex='^[А-Яа-яA-Za-z\\s]+$')], verbose_name='Название'),
        ),
    ]
