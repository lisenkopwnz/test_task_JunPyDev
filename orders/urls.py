from django.urls import path

from .api.endpoints import ApiOrderList, ApiOrderDetail, ApiOrderCreate, OrderUpdateView, RemoveDishFromOrderView, \
    OrderDeleteAPIView
from .views import OrderListView, CreateOrder, DeleteOrder, UpdateOrderStatus

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('create_order/', CreateOrder.as_view(), name='create_order'),
    path('delete_order/<int:pk>/', DeleteOrder.as_view(), name='delete_order'),  # Исправлено
    path('update-status/<int:order_id>/', UpdateOrderStatus.as_view(), name='update_status'),

    path('api/order_list', ApiOrderList.as_view(), name='api_order_list'),
    path('api/order/<int:id>/', ApiOrderDetail.as_view(), name='api_order_detail'),
    path('api/order/create/', ApiOrderCreate.as_view(), name='api_order_create'),
    path('api/order/update/<int:pk>/', OrderUpdateView.as_view(), name='api_order_update'),
    path('api/order/delete/<int:pk>/', OrderDeleteAPIView.as_view(), name='api_order_delete_api'),
    path('api/order/<int:order_id>/remove_dish/<int:dish_id>/', RemoveDishFromOrderView.as_view(), name='api_remove_dish_from_order'),

]