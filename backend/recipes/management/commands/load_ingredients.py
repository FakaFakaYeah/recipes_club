import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Начинаем импорт Ингредиентов")

        path = os.path.join(settings.BASE_DIR, "../data", "ingredients.json")
        print(path)
        ingredients = json.load(open(path, 'r', encoding="utf8"))

        Ingredient.objects.bulk_create(
            [Ingredient(**ingredient)
             for ingredient in ingredients]
        )

        print("Импорт ингредиентов успешно завершен.")