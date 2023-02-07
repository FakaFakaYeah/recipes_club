from django.urls import path, include
from rest_framework import routers

from .views import (
    IngredientsViewSet, TagViewSet, RecipeViewSet, subscribe, FollowList
)

router = routers.DefaultRouter()

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('users/subscriptions/', FollowList.as_view()),
    path('users/<int:author_id>/subscribe/', subscribe, name='subscriptions'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
