from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

router.register('ingredients', IngredientsViewset, basename='ingredients')
router.register('tags', TagViewset, basename='tags')

urlpatterns = [
    path('', include(router.urls))
]