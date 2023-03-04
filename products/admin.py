from django.contrib import admin
from products.models import ProductCategory, Product, Basket

# Register your models here.
admin.site.register(ProductCategory)


# указываем скаой модель будет работать admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'category')
    readonly_fields = ('description',)
    search_fields = ('name',)
    # сортировка по имени
    ordering = ('name',)


# admin.TabularInline  применяется если есть Forignkey связь
# теперь для пользователя  отброжается его корзина в админке
class BascketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0
