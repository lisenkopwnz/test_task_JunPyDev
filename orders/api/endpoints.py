from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from orders.api.filters import OrderFilter
from orders.api.pagination import OrderPagination
from orders.api.serializers import OrderSerializer
from orders.models import Order, OrderDish, Dish


class ApiOrderList(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch('order_dishes', queryset=OrderDish.objects.only('quantity', 'price_at_order', 'dish')),
            Prefetch('order_dishes__dish', queryset=Dish.objects.only('name', 'price')),
        ).only('id', 'table_number', 'status')
        return queryset
