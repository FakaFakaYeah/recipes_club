from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

router.register('users', CustomUserViewSet, basename='users')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
