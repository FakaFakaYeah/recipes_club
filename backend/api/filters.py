import django_filters

from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        to_field_name="slug",)
    is_favorited = django_filters.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = {'author', }

    def get_is_favorited(self, queryset, name, value):
        if value == 1:
            return queryset.filter(favourites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value == 1:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset
