import io

from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings

from recipes.models import (
    Ingredient, Tag, Recipe, Favourites, ShoppingCart, RecipeIngredient
)
from users.models import User, Follow
from .filters import RecipeFilter, IngredientsFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeReadSerializer,
    RecipeCreateSerializer, FollowSerializer, RecipeMiniSerializer
)
from .utils import universal_post, universal_delete, page_template


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
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            return universal_post(author, request.user, Follow,
                                  FollowSerializer, {'request': request},
                                  'author')
        return universal_delete(author, request.user, Follow, 'author')


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientsFilter,)
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

    def __get_recipe(self, pk):
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
        if request.method == 'POST':
            return universal_post(self.__get_recipe(pk), request.user,
                                  Favourites, RecipeMiniSerializer,
                                  context={'request': request})
        return universal_delete(self.__get_recipe(pk), request.user,
                                Favourites)

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return universal_post(self.__get_recipe(pk), request.user,
                                  ShoppingCart, RecipeMiniSerializer,
                                  context={'request': request})
        return universal_delete(self.__get_recipe(pk), request.user,
                                ShoppingCart)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoppingcart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount'))
        buffer = io.BytesIO()
        c = Canvas(buffer)
        pdfmetrics.registerFont(
            TTFont('Bad_Comic', 'Bad_Comic.ttf', 'UTF-8'))
        page_template(c)
        y = 700
        ingredient_number = 1
        for ingredient in ingredients:
            c.drawCentredString(35, y, str(ingredient_number))
            c.drawCentredString(200, y, f"{ingredient['ingredient__name']}")
            c.drawCentredString(380, y, f"{ingredient['amount']}")
            c.drawCentredString(
                500, y, f"{ingredient['ingredient__measurement_unit']}"
            )
            if ingredient_number % settings.ING_IN_PAGE == settings.ING_INDEX:
                c.showPage()
                page_template(c)
                y = 700
            y -= 25
            ingredient_number += 1
        c.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='Список покупок.pdf')
