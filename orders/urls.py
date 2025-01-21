from django.urls import path

from .api.endpoints import ApiOrderList, ApiOrderDetail
from .views import OrderListView, CreateOrder, DeleteOrder, UpdateOrderStatus

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create_order/', CreateOrder.as_view(), name='create_order'),
    path('delete_order/<int:pk>/', DeleteOrder.as_view(), name='delete_order'),  # Исправлено
    path('update-status/<int:order_id>/', UpdateOrderStatus.as_view(), name='update_status'),

    path('api/order_list', ApiOrderList.as_view(), name='api_order_list'),
    path('api/order/<int:id>/', ApiOrderDetail.as_view(), name='order-detail'),
]