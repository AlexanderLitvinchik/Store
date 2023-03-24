from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from users.models import User
from products.models import Product, ProductCategory


# Create your tests here.

# каждый метод должен начинать со слова text
class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        # содержит выполнение гет запроса
        response = self.client.get(path)
        print(response)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewCase(TestCase):
    # теперь когда создается тестовая база данных она заполняется данными из fixtures
    # какая проблема с кодировкой  в json   файлах
    fixtures = ['categories.json', 'goods.json']

    # таким образом выносятся переменные которые используются сразу в нескольких функциях
    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)
        self._common_tests(response)
        # без list вернет  quryset с одинаковым содержанием
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

        # дальше хотим проверить что на первлй странице отоброжаются первых три товара

    def test_list_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)
        self._common_tests(response)
        # без list вернет  quryset с одинаковым содержанием
        self.assertEqual(list(response.context_data['object_list']),
                         list(self.products.filter(category_id=category.id)))

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
