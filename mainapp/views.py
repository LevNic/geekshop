import os
import json
import random

from datetime import datetime

from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from mainapp.models import Product, ProductCategory
# from basketapp.models import Basket
from geekshop.settings import BASE_DIR


# Create your views here.

# Кеширование меню категорий
def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


# Кеширование категорий
def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product_item = cache.get(key)
        if product_item is None:
            product_item = get_object_or_404(Product, pk=pk)
            cache.set(key, product_item)
        return product_item
    else:
        return get_object_or_404(Product, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products_list = cache.get(key)
        if products_list is None:
            products_list = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products_list)
        return products_list
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products_list = cache.get(key)
        if products_list is None:
            products_list = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products_list)
        return products_list
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products_list = cache.get(key)
        if products is None:
            products_list = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products_list)
        return products_list
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def main(request):
    """ Главная страница """
    title = 'главная'

    # products_list = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    products_list = get_products()[:3]
    content = {
        'title': title,
        'products': products_list,
    }

    return render(request, 'mainapp/index.html', content)


def get_hot_product():
    products_hot = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
    return random.sample(list(products_hot), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk). \
                        select_related('category')[:3]
    return same_products


@cache_page(3600)
def products(request, pk=None, page=1):
    """Страница продукты"""

    title = 'продукты'
    links_menu = get_links_menu()

    # basket = []
    # if request.user.is_authenticated:
    #     basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            # products_list = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            products_list = get_products_orederd_by_price()
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            category = get_category(pk)
            # products_list = Product.objects.filter(category__pk=pk, is_active=True,
            # category__is_active=True).order_by('price')
            products_list = get_products_in_category_orederd_by_price(pk)
        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,

        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    """Страница контакты"""
    title = 'о нас'
    visit_date = datetime.now()
    location = None
    with open(os.path.join(BASE_DIR, 'mainapp/json/contact__locations.json')) as f:
        location = json.load(f)
    content = {
        'title': title,
        'visit_date': visit_date,
        'location': location,
    }
    return render(request, 'mainapp/contact.html', content)


def not_found(request, exceptiion):
    content = {
        'product': Product.object.all()[:3]
    }
    return render(request, '', content)


def product(request, pk):
    links_menu = get_links_menu()
    # links_menu = ProductCategory.objects.filter(is_active=True)

    # product_item = get_object_or_404(Product, pk=pk)
    product_item = get_product(pk)

    content = {
        'title': product_item.name,
        'links_menu': links_menu,
        'product': product_item,
        'same_products': get_same_products(product_item),
    }

    return render(request, 'mainapp/product.html', content)


def load_from_json(file_name):
    JSON_PATH = 'json/'
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', errors='ignore') as infile:
        return json.load(infile)
