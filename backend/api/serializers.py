from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer, UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    Tag, Ingredient, Recipe, RecipeIngredient, Favourites, ShoppingCart
)
from users.models import Follow, User


class CustomCreateUserSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя"""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор для получения пользователей"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return (
                self.context['request'].user.is_authenticated
                and Follow.objects.filter(author=obj,
                                          user=self.context['request'].user
                                          ).exists()
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов """
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов"""
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка ингредиентов"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания списка ингредиентов"""
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/редактирования/удаления рецептов"""
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipeingredient_set'
    )
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        return (
                self.context['request'].user.is_authenticated
                and Favourites.objects.filter(
                  recipe=obj,
                  user=self.context['request'].user
                  ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
                self.context['request'].user.is_authenticated
                and ShoppingCart.objects.filter(
                  recipe=obj,
                  user=self.context['request'].user
                ).exists()
        )


class RecipeCreateSerializer(RecipeReadSerializer):
    """Сериализатор для работы с рецептами"""
    ingredients = RecipeIngredientCreateSerializer(many=True,
                                                   allow_empty=False)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, allow_empty=False
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )

    @staticmethod
    def add_tags_and_ingredients(recipe, tags, ingredients):
        recipe.tags.set(tags)
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(recipe=recipe,
                              ingredient=get_object_or_404(
                                  Ingredient, pk=ingredient['id']),
                              amount=ingredient['amount'])
             for ingredient in ingredients]
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
        ingredient_id = [ingredient.get('id') for ingredient in ingredients]
        if len(ingredient_id) != len(set(ingredient_id)):
            raise serializers.ValidationError(
                'Ингредиент можно добавить только один раз!'
            )
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        self.add_tags_and_ingredients(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.add_tags_and_ingredients(instance, tags, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data


class RecipeMiniSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецепта в упрощенной форме"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(CustomUserSerializer):
    """Сериализатор для подписок/отписок"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipes.count')

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        queryset = obj.recipes.all()
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return RecipeMiniSerializer(queryset, many=True).data
