from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега'
    )
    color = ColorField(
        unique=True,
        max_length=7,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/images',
        verbose_name='Фото'
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание вашего рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                settings.MIN_COOK_TIME,
                message='Нельзя готовить меньше одной минуты!'
            ),
            MaxValueValidator(
                settings.MAX_COOK_TIME,
                message='Нельзя готовить блюдо неделю!'
            )
        ],
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления рецепта'
    )

    class Meta:
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                settings.MIN_AMOUNT,
                message='Неправильная величина продукта!'
            )
        ]
    )

    class Meta:
        verbose_name_plural = 'Рецепты + ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'], name='unique_ingredient'
            )
            ]

    def __str__(self):
        return f'{self.ingredient} --> {self.recipe}'


class BaseFavouritesAndShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Кто добавляет'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Рецепт'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время добавления'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'], name='unique_add'
            )
        ]

    def __str__(self):
        return f'{self.user} --- > {self.recipe}'


class Favourites(BaseFavouritesAndShoppingCart):

    class Meta(BaseFavouritesAndShoppingCart.Meta):
        verbose_name_plural = 'Любимые рецепты'


class ShoppingCart(BaseFavouritesAndShoppingCart):

    class Meta(BaseFavouritesAndShoppingCart.Meta):
        verbose_name_plural = 'Рецепты в списке покупок'
