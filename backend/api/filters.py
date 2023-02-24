from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр для рецептов. Поиск slug тэга,
    любимым рецептам и рецептам в списке покупок."""

    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        to_field_name="slug", )
    is_favorited = rest_framework.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'tags')

    def get_recipes(self, related_name):
        recipes = getattr(self.request.user, related_name).values_list(
            'recipe', flat=True
        )
        return Recipe.objects.filter(id__in=recipes)

    def get_is_favorited(self, queryset, name, value):
        if value:
            return self.get_recipes('favourites')
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return self.get_recipes('shoppingcart')
        return queryset


class IngredientsFilter(SearchFilter):
    """Фильтр для поиска ингредиентов по названию."""

    search_param = 'name'
