import os

import json
import random

from datetime import datetime

from django.shortcuts import render, get_list_or_404, get_object_or_404
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket
from geekshop.settings import BASE_DIR
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def main(request):
    ''' Главная страница '''
    title = 'главная'

    products_list = Product.objects.all()[:3]

    content = {
        'title': title,
        'products': products_list,
    }

    return render(request, 'mainapp/index.html', content)


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).\
        exclude(pk=hot_product.pk)[:3]

    return same_products


def products(request, pk=None, page=1):
    '''Страница продукты'''

    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk,
                                              is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
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
    '''Страница контакты'''
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
    product_item = get_object_or_404(Product, pk=pk)

    content = {
        'title': product_item.name,
        'links_menu': ProductCategory.objects.all(),
        'product': product_item,
        'same_products': get_same_products(product_item),
    }

    return render(request, 'mainapp/product.html', content)
