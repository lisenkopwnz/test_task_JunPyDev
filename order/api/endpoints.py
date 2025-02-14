from django.db.models import Prefetch, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
import logging

from order.api.filters import OrderFilter
from order.api.pagination import OrderPagination
from order.api.serializers import OrderSerializer, OrderCreateUpdateSerializer, DishSerializer
from order.models import Order, OrderDish, Dish


logger = logging.getLogger(__name__)


class OrderQuerysetMixin:
    """
    Миксин для оптимизации запросов к Order.
    Добавляет prefetch_related и only для уменьшения количества запросов к БД.
    """

    def get_queryset(self) -> QuerySet[Order]:
        """
        Возвращает оптимизированный QuerySet для Order.
        """
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch('order_dishes', queryset=OrderDish.objects.only('quantity', 'price_at_order', 'dish')),
            Prefetch('order_dishes__dish', queryset=Dish.objects.only('name', 'price')),
        ).only('id', 'table_number', 'status')
        return queryset


class ApiOrderList(OrderQuerysetMixin, ListAPIView):
    """
    API для получения списка заказов.
    Поддерживает фильтрацию и пагинацию.

    Пример запроса:
    ```
    curl -X GET http://localhost:8000/api/order_list/
    ```

    Пример запроса с фильтрацией:
    ```
    curl -X GET "http://localhost:8000/api/order_list/?table_number=5&status=pending"
    ```
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter


class ApiOrderDetail(OrderQuerysetMixin, RetrieveAPIView):
    """
    API для получения деталей конкретного заказа.

    Пример запроса:
    ```
    curl -X GET http://localhost:8000/api/order/1/
    ```
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'


class ApiOrderCreate(CreateAPIView):
    """
    API для создания нового заказа.

    Пример запроса:
    ```
    curl -X POST http://localhost:8000/api/order/create/ \\
    -H "Content-Type: application/json" \\
    -d '{
        "table_number": 5,
        "status": "pending",
        "items": [
            {
                "dish": 1,
                "quantity": 2,
                "price_at_order": 10.99
            },
            {
                "dish": 2,
                "quantity": 1,
                "price_at_order": 5.99
            }
        ]
    }'
    ```
    """

    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer

    def perform_create(self, serializer: OrderCreateUpdateSerializer) -> None:
        """
        Сохраняет заказ и логирует его создание.
        """
        order = serializer.save()
        logger.info(f"Заказ {order.id} успешно создан.")


class ApiOrderUpdate(UpdateAPIView):
    """
    API для обновления существующего заказа.

    Пример запроса (PUT):
    ```
    curl -X PUT http://localhost:8000/api/order/update/1/ \\
    -H "Content-Type: application/json" \\
    -d '{
        "table_number": 5,
        "status": "completed",
        "items": [
            {
                "dish": 1,
                "quantity": 3,
                "price_at_order": 10.99
            }
        ]
    }'
    ```

    Пример запроса (PATCH):
    ```
    curl -X PATCH http://localhost:8000/api/order/update/1/ \\
    -H "Content-Type: application/json" \\
    -d '{
        "status": "completed"
    }'
    ```
    """

    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer

    def perform_update(self, serializer: OrderCreateUpdateSerializer) -> None:
        """
        Сохраняет обновленный заказ и логирует изменения.
        """
        order = serializer.save()
        logger.info(f"Заказ {order.id} успешно обновлен.")


class ApiOrderDelete(DestroyAPIView):
    """
    API для удаления заказа.

    Пример запроса:
    ```
    curl -X DELETE http://localhost:8000/api/order/delete/1/
    ```
    """

    queryset = Order.objects.all()
    lookup_field = 'pk'

    def perform_destroy(self, instance: Order) -> None:
        """
        Удаляет заказ и логирует его удаление.
        """
        logger.info(f"Заказ {instance.id} успешно удален.")
        instance.delete()


class ApiRemoveDishFromOrder(APIView):
    """
    API для удаления блюда из заказа.

    Пример запроса:
    ```
    curl -X DELETE http://localhost:8000/api/order/1/remove_dish/2/
    ```
    """

    def delete(self, request: Request, order_id: int, dish_id: int) -> Response:
        """
        Удаляет блюдо из заказа и пересчитывает общую стоимость.
        """
        try:
            # Находим заказ
            order = Order.objects.get(pk=order_id)
            # Находим связь между заказом и блюдом
            order_dish = OrderDish.objects.filter(order=order, dish_id=dish_id).first()
            if order_dish:
                # Удаляем связь
                order_dish.delete()
                # Пересчитывается общая стоимость
                order.calculate_total_price()
                logger.info(f"Блюдо {dish_id} удалено из заказа {order_id}.")
                return Response({"detail": "Блюдо удалено из заказа."}, status=status.HTTP_204_NO_CONTENT)
            else:
                logger.warning(f"Блюдо {dish_id} не найдено в заказе {order_id}.")
                return Response({"detail": "Блюдо не найдено в заказе."}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            logger.error(f"Заказ {order_id} не найден.")
            return Response({"detail": "Заказ не найден."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Ошибка при удалении блюда из заказа: {str(e)}")
            return Response({"detail": "Произошла ошибка на сервере."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DishViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Dish.
    Обрабатывает все CRUD-операции:
    - Создание (POST)
    - Чтение списка (GET)
    - Чтение одного объекта (GET)
    - Обновление (PUT)
    - Удаление (DELETE)

    Пример запроса для создания блюда (POST):
    ```
    curl -X POST http://localhost:8000/api/dishes/ \\
    -H "Content-Type: application/json" \\
    -d '{
        "name": "Pizza",
        "price": 10.99
    }'
    ```

    Пример запроса для получения списка блюд (GET):
    ```
    curl -X GET http://localhost:8000/api/dishes/
    ```

    Пример запроса для обновления блюда (PUT):
    ```
    curl -X PUT http://localhost:8000/api/dishes/1/ \\
    -H "Content-Type: application/json" \\
    -d '{
        "name": "Pizza",
        "price": 12.99
    }'
    ```

    Пример запроса для удаления блюда (DELETE):
    ```
    curl -X DELETE http://localhost:8000/api/dishes/1/
    ```
    """

    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    pagination_class = OrderPagination

    def perform_create(self, serializer: DishSerializer) -> None:
        """
        Сохраняет новое блюдо и логирует его создание.
        """
        dish = serializer.save()
        logger.info(f"Блюдо {dish.id} успешно создано.")

    def perform_update(self, serializer: DishSerializer) -> None:
        """
        Сохраняет обновленное блюдо и логирует изменения.
        """
        dish = serializer.save()
        logger.info(f"Блюдо {dish.id} успешно обновлено.")

    def perform_destroy(self, instance: Dish) -> None:
        """
        Удаляет блюдо и логирует его удаление.
        """
        logger.info(f"Блюдо {instance.id} успешно удалено.")
        instance.delete()
