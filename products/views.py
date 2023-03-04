from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Basket
from users.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    context = {
        'title': 'Store',
        'username': 'valeriy'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_number=1):
    # если пришел параметр  category_id
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    # первый список , второй парметр  сколько товар нужно отрброжатьна странице
    per_page = 3
    paginator = Paginator(products, per_page)
    # передается страница, products_paginator помимо метод productбудет иметь еще и свои например get_page next_page
    products_paginator = paginator.page(page_number)
    context = {
        'title': 'Store - Каталог',
        'products': products_paginator,
        'categories': ProductCategory.objects.all()
    }
    return render(request, 'products/products.html', context)


# @login_required(login_url=) если пользовватель не аутифициорован
# то мы его нарпвляем на страницу авторизации либо через  login_url=куда напрвить
# или в settings.py  присваиваем LOGIN_URL= '/users/login/'(нужное значение)
@login_required
# добовление в корзину
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    # берем все корзины пользователся с опредленным продуктом
    # по скти корзина это типо продукт(с разными полями)
    # и здесь вернется масимум один элемент так как конктреный продукт для контрного пользователя
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    # товар модноо добовлять в разных местах поэтому
    # должны пернаправлять туда откуда мы и пришли
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
