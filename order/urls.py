from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api.endpoints import (
    ApiOrderList, ApiOrderDetail, ApiOrderCreate,
    ApiOrderUpdate, ApiOrderDelete, ApiRemoveDishFromOrder, DishViewSet,
)
from .views import (OrderListView, CreateOrder,
                    DeleteOrder, UpdateOrderStatus,
                    MenuListView, DishCreate, DishDelete, DishUpdate
                    )

app_name = 'orders'

# роутер для DishViewSet
router = DefaultRouter()
router.register(r'dish', DishViewSet, basename='dish')

# URL-адреса для веб-интерфейса
web_urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),  # Список заказов
    path('create_order/', CreateOrder.as_view(), name='create_order'),  # Создание заказа
    path('delete_order/<int:pk>/', DeleteOrder.as_view(), name='delete_order'),  # Удаление заказа
    path('update-status/<int:order_id>/', UpdateOrderStatus.as_view(), name='update_status'),  # Обновление статуса заказа
    path('menu/', MenuListView.as_view(),  name='menu_list'),  # маршрут для меню
    path('delete_dish/<int:pk>/', DishDelete.as_view(), name='delete_dish'),  # Маршрут для удаления блюда
    path('create_dish/', DishCreate.as_view(), name='create_dish'),  # маршрут для создания блюда
    path('update_dish/<int:pk>/', DishUpdate.as_view(), name='update_dish'),  # маршрут для изменения блюда
]

# URL-адреса для API

api_urlpatterns = [
    path('order_list/', ApiOrderList.as_view(), name='api_order_list'),  # Список заказов (API)
    path('order/<int:id>/', ApiOrderDetail.as_view(), name='api_order_detail'),  # Детали заказа (API)
    path('order/create/', ApiOrderCreate.as_view(), name='api_order_create'),  # Создание заказа (API)
    path('order/update/<int:pk>/', ApiOrderUpdate.as_view(), name='api_order_update'),  # Обновление заказа (API)
    path('order/delete/<int:pk>/', ApiOrderDelete.as_view(), name='api_order_delete_api'),  # Удаление заказа (API)
    path('order/<int:order_id>/remove_dish/<int:dish_id>/', ApiRemoveDishFromOrder.as_view(),
         name='api_remove_dish_from_order'),  # Удаление блюда из заказа (API)
]

# Объединение всех URL-адресов
urlpatterns = web_urlpatterns + [
    path('api/', include(api_urlpatterns)),
    path('api/', include(router.urls)),
]