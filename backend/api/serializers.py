from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from foodgram.settings import SIZE_IMAGE
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from users.models import User


class UserReadSerializer(UserSerializer):
    """Сериализатор для получения пользователей"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (user.is_authenticated
                and user.follower.filter(author=obj).exists())


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
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для создания/редактирования/удаления рецептов"""
    ingredients = RecipeIngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    author = UserReadSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def check_method(self, obj, related_name):
        user = self.context['request'].user
        return (user.is_authenticated
                and getattr(user, related_name).filter(recipe=obj).exists())

    def get_is_favorited(self, obj):
        return self.check_method(obj, 'favourites')

    def get_is_in_shopping_cart(self, obj):
        return self.check_method(obj, 'shoppingcart')


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
    def validate_image(value):
        if value.size > 0.1 * 1024 * 1024:
            raise serializers.ValidationError(
                'Картинки размером больше 1Mb не поддерживаются'
            )

    @staticmethod
    def add_tags_and_ingredients(recipe, tags, ingredients):
        recipe.tags.set(tags)
        try:
            RecipeIngredient.objects.bulk_create(
                [RecipeIngredient(recipe=recipe,
                                  ingredient=ingredient['id'],
                                  amount=ingredient['amount'])
                 for ingredient in ingredients]
            )
        except KeyError:
            raise serializers.ValidationError(
                'Укажите хотя бы один ингредиент!'
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


class FollowSerializer(UserReadSerializer):
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
            try:
                queryset = queryset[:int(recipes_limit)]
            except ValueError:
                raise serializers.ValidationError('В лимите рецептов не число')
        return RecipeMiniSerializer(queryset, many=True).data
