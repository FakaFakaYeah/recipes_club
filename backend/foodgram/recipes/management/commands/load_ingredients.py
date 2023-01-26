import os
import json

from django.core.management import BaseCommand
from recipes.models import Ingredients

from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Import Ingredients data")

        path = os.path.join(settings.BASE_DIR, "../../data", "ingredients.json")
        print(path)
        ingredients = json.load(open(path, 'r', encoding="utf8"))

        for ingredient in ingredients:
            Ingredients.objects.create(**ingredient)

        print("Import Ingredients data done")