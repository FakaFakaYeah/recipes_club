# Generated by Django 2.2.16 on 2023-02-10 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20230210_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Только буквы, пробелы разрешены.', max_length=200, unique=True, verbose_name='Название тега'),
        ),
    ]
