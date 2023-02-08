from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Фильтр для рецептов. Поиск slug тэга,
    любимым рецептам и рецептам в списке покупок."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        to_field_name="slug",)
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = {'author'}

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return self.request.user.favourites.values('recipe')
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return self.request.user.shoppingcart.values('recipe')
        return queryset


class IngredientsFilter(SearchFilter):
    """Фильтр для поиска ингредиентов по названию."""

    search_param = 'name'
