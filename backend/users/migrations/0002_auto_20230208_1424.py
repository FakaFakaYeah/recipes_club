# Generated by Django 2.2.16 on 2023-02-08 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name_plural': 'Подписки'},
        ),
        migrations.RemoveField(
            model_name='follow',
            name='pub_date',
        ),
    ]