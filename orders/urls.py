from django.urls import path
from .views import OrderListView, CreateOrder, DeleteOrder

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create_order/', CreateOrder.as_view(), name='create_order'),
    path('delete_order/<int:pk>/', DeleteOrder.as_view(), name='delete_order'),  # Исправлено
]