import json
import os

from colorama import Fore, Style
from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда по загрузке ингредиентов"""
    def handle(self, *args, **options):
        print(Fore.GREEN + 'Начинаем импорт ингредиентов!')
        try:
            path = os.path.join(settings.BASE_DIR, "./", "ingredients.json")
            ingredients = json.load(open(path, 'r', encoding="utf8"))
            Ingredient.objects.bulk_create(
                [Ingredient(**ingredient)
                 for ingredient in ingredients], ignore_conflicts=True
            )
            print(Fore.GREEN + 'Импорт успешно завершен' + Style.RESET_ALL)
        except FileNotFoundError:
            print(Fore.RED + 'Файл с данными не найден' + Style.RESET_ALL)
