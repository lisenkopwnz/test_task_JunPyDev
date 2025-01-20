from django.urls import path

from orders.views import OrderListView, CreateOrder

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create_order/', CreateOrder.as_view(), name='create_order')
]