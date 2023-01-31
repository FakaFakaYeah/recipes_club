from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import Ingredient, Tag, Recipe, Favourites, ShoppingCart
from users.models import User, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeReadSerializer,
    RecipeCreateSerializer, FollowSerializer, RecipeMiniSerializer
)
from .pagination import CustomPagination
from .filters import RecipeFilter


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'delete')
    pagination_class = CustomPagination

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        page = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = FollowSerializer(page, many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        subscription = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                return Response({'error': 'Нельзя подписываться на себя!'},
                                status=status.HTTP_400_BAD_REQUEST)
            elif subscription.exists():
                return Response({'error': 'Вы уже подписаны на пользователя!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not subscription.exists():
                return Response({'error': 'Вы не подписаны на пользователя!'},
                                status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favourites.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if favorite.exists():
                return Response({'error': 'Рецепт уже добавлен в избранное!'},
                                status=status.HTTP_400_BAD_REQUEST)
            Favourites.objects.create(user=user, recipe=recipe)
            serializer = RecipeMiniSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not favorite.exists():
                return Response({'error': 'Этого рецепта нет в избранном!'},
                                status=status.HTTP_400_BAD_REQUEST)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if shopping_cart.exists():
                return Response({'error': 'Рецепт уже добавлен в покупки!'},
                                status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeMiniSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not shopping_cart.exists():
                return Response({'error': 'Этого рецепта нет в покупках!'},
                                status=status.HTTP_400_BAD_REQUEST)
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
