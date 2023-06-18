import os
import json

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Команда для импорта данных из .csv в базу данных проекта'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь до csv-файла')

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Данные некорректны')
        
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError('Неверно передан путь до .csv')

        with open(csv_file_path, 'r', encoding='UTF-8') as f:
            data = json.load(f)

            for item in data:
                ingredients = Ingredient(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                )
                ingredients.save()
