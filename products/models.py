import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.

class ProductCategory(models.Model):
    # unique озночает что каждая категория уникальна
    name = models.CharField(max_length=128, unique=True)
    # параматры говорят что поле может быть пустым
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    #для отоброжения в админке странно что здесь пишем
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    # 6 цифр до запятой и после запятой 2 цефры с округлением
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    # CASCADE означает что при удалении всей категори удалться и все продукты из этой категории
    # Protect запрещает удалять всю категорию чтобы вся категория удалиласть на удалитьвсе продукты по отдельности
    # SET_DEFAULT при удалении категории в данную категори ю поставиться значение по умолчанию
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
    def __str__(self):
        return f'Продукт: {self.name}| Категория: {self.category.name} '

    #для отоброжения в админке странно что здесь пишем

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub')
        return stripe_product_price

# для того чтобы total_sum и total qauntity раьотали
class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    # как только создается объект сразу ставится время
    created_timestamp = models.DateTimeField(auto_now_add=True)
    # для того чтобы total_sum и total qauntity раьотали
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username}| Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
