from django.shortcuts import render
from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from django.urls import reverse_lazy
from common.views import TitleMixin

# Create your views here.


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order-create')
    title = 'Store - оформление заказа'

    def form_valid(self, form):
        #instance сам объект (честно говоря не понимаю почему не  удается получить пользователся
        # в самой модели )
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
