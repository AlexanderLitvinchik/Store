from django.urls import path
from orders.views import OrderDetailView, OrderListView, OrderCreateView, SuccessTemplateView, CanceledTemplateView

app_name = 'orders'
urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),

]
