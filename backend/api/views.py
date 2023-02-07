from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from recipes.models import (
    Ingredient, Tag, Recipe, Favourites, ShoppingCart, RecipeIngredient
)
from users.models import User, Follow
from .filters import RecipeFilter, IngredientsFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeReadSerializer,
    RecipeCreateSerializer, RecipeMiniSerializer, FollowSerializer
)
from .utils import universal_post, universal_delete, shopping_cart_page_create


class FollowList(ListAPIView):
    """Получение списка подписок"""
    serializer_class = FollowSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscribe(request, author_id=None):
    """Метод подписки и отписки на авторов"""
    filter_params = {'user': request.user,
                     'author': get_object_or_404(User, pk=author_id)}
    if request.method == 'POST':
        return universal_post(filter_params, Follow, filter_params['author'],
                              FollowSerializer, {'request': request})
    return universal_delete(filter_params, Follow, filter_params['author'])


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientsFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тэгов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами, добавлением их в
    избранное и список покупок + скачивание списка покупок"""
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    @staticmethod
    def __get_recipe(pk):
        return get_object_or_404(Recipe, pk=pk)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        filter_params = {'user': request.user, 'recipe': self.__get_recipe(pk)}
        if request.method == 'POST':
            return universal_post(
                filter_params, Favourites, filter_params['recipe'],
                RecipeMiniSerializer, {'request': request}
            )
        return universal_delete(
            filter_params, Favourites, filter_params['recipe']
        )

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        filter_params = {'user': request.user, 'recipe': self.__get_recipe(pk)}
        if request.method == 'POST':
            return universal_post(
                filter_params, ShoppingCart, filter_params['recipe'],
                RecipeMiniSerializer, {'request': request}
            )
        return universal_delete(
            filter_params, ShoppingCart, filter_params['recipe']
        )

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoppingcart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount'))
        return shopping_cart_page_create(ingredients)
