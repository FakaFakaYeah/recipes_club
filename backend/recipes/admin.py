from django.contrib import admin
from django.utils.html import format_html

from .models import Ingredient, Tag, Recipe, RecipeIngredient, Favourites


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class IngredientInRecipeInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class Recipes(admin.ModelAdmin):
    inlines = [
        IngredientInRecipeInline,
    ]
    list_display = (
        'name', 'author', 'image', 'text', 'cooking_time', 'pub_date'
    )
    filter_horizontal = ('tags',)
    readonly_fields = ('image_preview',)

    def image_preview(self, image_preview):
        return format_html(
            '<img src="/media/{}" height=200px width=auto />',
            image_preview.image
        )

    image_preview.short_description = 'Фото рецепта'


@admin.register(RecipeIngredient)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pub_date')
