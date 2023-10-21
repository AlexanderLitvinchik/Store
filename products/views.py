from django.shortcuts import render, HttpResponseRedirect
from products.models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from common.views import TitleMixin
from django.views.generic.list import ListView
from django.core.cache import cache
from users.models import User
from django.core.paginator import Paginator


# Create your views here.
class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог  '

    def get_queryset(self):
        # Product.objects.all()
        queryset = super(ProductListView, self).get_queryset()
        # все дополнительные параметры котрые передаются хранятся в  kwargs
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    # получается что у пользователя много корзин, для каждого продукта своя корзина,
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    # товар можно добовлять в разных местах поэтому
    # должны пернаправлять туда откуда мы и пришли
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

# def index(request):
#     context = {
#         'title': 'Store',
#         'username': 'valeriy'
#     }
#     return render(request, 'products/index.html', context)


# def products(request, category_id=None, page_number=1):
#     # если пришел параметр  category_id
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#     # первый список , второй парметр  сколько товар нужно отрброжатьна странице
#     per_page = 3
#     paginator = Paginator(products, per_page)
#     # передается страница, products_paginator помимо метод product будет иметь еще и свои например get_page next_page
#     products_paginator = paginator.page(page_number)
#     context = {
#         'title': 'Store - Каталог',
#         'products': products_paginator,
#         'categories': ProductCategory.objects.all()
#     }
#     return render(request, 'products/products.html', context)


# @login_required(login_url=) если пользовватель не аутифициорован
# то мы его нарпвляем на страницу авторизации либо через  login_url=куда напрвить
# или в settings.py  присваиваем LOGIN_URL= '/users/login/'(нужное значение)
