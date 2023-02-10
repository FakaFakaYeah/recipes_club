from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Ingredient, Tag, Recipe, RecipeIngredient, Favourites, ShoppingCart
)


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    """Админ панель для ингредиентов"""
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админ панель для тэгов"""
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class IngredientInRecipeInline(admin.TabularInline):
    """Позволяет добавлять ингредиенты на странице рецепта"""
    model = RecipeIngredient
    min_num = 1


@admin.register(Recipe)
class Recipes(admin.ModelAdmin):
    """Админ панель для рецептов"""
    inlines = (IngredientInRecipeInline,)
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags',)
    readonly_fields = ('image_preview', 'favourites')

    def image_preview(self, image_preview):
        return format_html(
            '<img src="/media/{}" height=200px width=auto />',
            image_preview.image
        )
    image_preview.short_description = 'Фото рецепта'

    def favourites(self, obj):
        return obj.favourites.count()
    favourites.short_description = 'В избранном'


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    """Админ панель для избранных рецептов"""
    list_display = ('__str__', 'pub_date')
    list_filter = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админ панель для списка покупок"""
    list_display = ('__str__', 'pub_date')
    list_filter = ('user',)
