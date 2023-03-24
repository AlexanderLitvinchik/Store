from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    # не совсем понятно зачем эти данные переносить сюда когда можно это указать в самом шаблоне
    # избовляемся от дной строчкии в шаблоне но надо добовлять в label id_for_label
    # не совсем ясен смысл данного действия
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}))
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Россия, Москва, ул. Мира, дом 6'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
