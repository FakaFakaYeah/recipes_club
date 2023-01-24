from django.db import models


class Ingredients(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=15,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
