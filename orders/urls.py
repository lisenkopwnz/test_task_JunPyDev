from django.urls import path, include
from .api.endpoints import (
    ApiOrderList, ApiOrderDetail, ApiOrderCreate, OrderUpdateView,
    RemoveDishFromOrderView, OrderDeleteAPIView
)
from .views import OrderListView, CreateOrder, DeleteOrder, UpdateOrderStatus

app_name = 'orders'

# URL-адреса для веб-интерфейса
web_urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),  # Список заказов
    path('create_order/', CreateOrder.as_view(), name='create_order'),  # Создание заказа
    path('delete_order/<int:pk>/', DeleteOrder.as_view(), name='delete_order'),  # Удаление заказа
    path('update-status/<int:order_id>/', UpdateOrderStatus.as_view(), name='update_status'),  # Обновление статуса заказа
]

# URL-адреса для API
api_urlpatterns = [
    path('order_list/', ApiOrderList.as_view(), name='api_order_list'),  # Список заказов (API)
    path('order/<int:id>/', ApiOrderDetail.as_view(), name='api_order_detail'),  # Детали заказа (API)
    path('order/create/', ApiOrderCreate.as_view(), name='api_order_create'),  # Создание заказа (API)
    path('order/update/<int:pk>/', OrderUpdateView.as_view(), name='api_order_update'),  # Обновление заказа (API)
    path('order/delete/<int:pk>/', OrderDeleteAPIView.as_view(), name='api_order_delete_api'),  # Удаление заказа (API)
    path('order/<int:order_id>/remove_dish/<int:dish_id>/', RemoveDishFromOrderView.as_view(),
         name='api_remove_dish_from_order'),  # Удаление блюда из заказа (API)
]

# Объединение всех URL-адресов
urlpatterns = web_urlpatterns + [
    path('api/', include(api_urlpatterns)),  # Группировка API-адресов под префиксом /api/
]