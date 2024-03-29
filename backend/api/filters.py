from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Фильтр для рецептов. Поиск slug тэга,
    любимым рецептам и рецептам в списке покупок."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        to_field_name="slug", )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'tags')

    def get_recipes(self, related_name, queryset):
        recipes = getattr(self.request.user, related_name).values_list(
            'recipe', flat=True
        )
        return queryset.filter(id__in=recipes)

    def get_is_favorited(self, queryset, name, value):
        if value:
            return self.get_recipes('favourites', queryset)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return self.get_recipes('shoppingcart', queryset)
        return queryset


class IngredientsFilter(SearchFilter):
    """Фильтр для поиска ингредиентов по названию."""

    search_param = 'name'
