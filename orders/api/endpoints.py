from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.api.filters import OrderFilter
from orders.api.pagination import OrderPagination
from orders.api.serializers import OrderSerializer, OrderCreateUpdateSerializer
from orders.models import Order, OrderDish, Dish


class OrderQuerysetMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch('order_dishes', queryset=OrderDish.objects.only('quantity', 'price_at_order', 'dish')),
            Prefetch('order_dishes__dish', queryset=Dish.objects.only('name', 'price')),
        ).only('id', 'table_number', 'status')
        return queryset

class ApiOrderList(OrderQuerysetMixin,ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

class ApiOrderDetail(OrderQuerysetMixin,RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'

class ApiOrderCreate(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer

class OrderUpdateView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateUpdateSerializer

class OrderDeleteAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    lookup_field = 'pk'


class RemoveDishFromOrderView(APIView):
    def delete(self, request, order_id, dish_id):
        try:
            # Находим заказ
            order = Order.objects.get(pk=order_id)
            # Находим связь между заказом и блюдом
            order_dish = OrderDish.objects.filter(order=order, dish_id=dish_id).first()
            if order_dish:
                # Удаляем связь
                order_dish.delete()
                # Пересчитываем общую стоимость
                order.calculate_total_price()
                return Response({"detail": "Блюдо удалено из заказа."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "Блюдо не найдено в заказе."}, status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            return Response({"detail": "Заказ не найден."}, status=status.HTTP_404_NOT_FOUND)
