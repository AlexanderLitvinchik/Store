"""Store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products.views import IndexView
# для отброжения фотограий
from django.conf.urls.static import static
# cделали именно так чтобы подтянуть все настройки
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    # path('accounts/', include(('users.urls', 'users'), namespace='users')),
    # в include вторым апараметром пишется имя приложения не понятно почему(если не писать то вообще работать не будет)
    # namespace позволяет оброщаться к url  через namesppace в шаблонах
    # напрмер чтобы вызывать функцию index из приложения products надо написть
    # {% url 'products:index' %}
    path('products/', include(('products.urls', 'products'), namespace='products')),

    # когда перешли к классам CBV почемув адрессе вместо users  начало отброжаться accounts
    # не понятно почему так работает
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('accounts/', include('allauth.urls')),
]

# если находимся на этапе разработки а не на prodactions
if settings.DEBUG:
    #для каширование
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
