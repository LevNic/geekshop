'''Комманда загрузки данных в БД из файла'''

import os
import json

from django.conf import settings
from django.core.management import BaseCommand
# from django.contrib.auth.models import User

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


def load_from_json(file_name):
    '''Загрузка данных из json-файла'''
    file_path = os.path.join(
        settings.BASE_DIR, 'mainapp/json/') + file_name + '.json'
    with open(file_path, 'r', encoding='utf-8') as f_json:
        return json.load(f_json)


class Command(BaseCommand):
    '''Класс команд'''

    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all().delete()
        for cat in categories:
            ProductCategory.objects.create(**cat)

        products = load_from_json('products')
        Product.objects.all().delete()
        for prod in products:
            cat_name = prod['category']
            _cat = ProductCategory.objects.get(name=cat_name)
            prod['category'] = _cat
            Product.objects.create(**prod)

        ShopUser.objects.create_superuser(
            username='django', password='geekbrains', age=30)
