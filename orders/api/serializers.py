from rest_framework import serializers

from orders.models import Dish, OrderDish, Order


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']

class OrderDishSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)

    class Meta:
        model = OrderDish
        fields = ['dish', 'quantity', 'price_at_order']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderDishSerializer(source='order_dishes', many=True, read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']
