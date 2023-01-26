from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from .models import User, Follow


class CustomCreateUserSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                'Такой пользователь уже существует'
            )
        return value


class CustomUserSerializer(UserSerializer):
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


class FollowSerializer(CustomUserSerializer):

    recipes = serializers.CharField(read_only=True, default='Рецепт')
    recipes_count = serializers.IntegerField(read_only=True, default=10)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )
