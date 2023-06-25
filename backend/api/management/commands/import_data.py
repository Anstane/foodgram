import os
import json

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Команда для импорта данных в базу данных проекта.'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Путь до json-файла.')

    def handle(self, *args, **options):
        json_file_path = options['file']

        if not os.path.exists(json_file_path):
            raise CommandError('Неверно передан путь до файла с данными.')

        with open(json_file_path, 'r', encoding='UTF-8') as f:
            data = json.load(f)

            for item in data:
                ingredients = Ingredient(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                )
                ingredients.save()
