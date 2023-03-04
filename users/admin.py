from django.contrib import admin
from .models import User
from products.admin import BascketAdmin

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BascketAdmin,)
