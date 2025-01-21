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

class OrderDishCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDish
        fields = ['dish', 'quantity', 'price_at_order']

class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    items = OrderDishCreateUpdateSerializer(source='order_dishes', many=True, required=False)

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('order_dishes')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderDish.objects.create(
                order=order,
                dish=item_data['dish'],
                quantity=item_data['quantity'],
                price_at_order=item_data['price_at_order']  # Используем правильное имя поля
            )
        order.calculate_total_price()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('order_dishes', None)

        # Обновляем table_number, если оно передано
        if 'table_number' in validated_data:
            instance.table_number = validated_data['table_number']

        # Обновляем статус, если он передан
        if 'status' in validated_data:
            instance.status = validated_data['status']

        # Обновляем список блюд, если он передан
        if items_data is not None:
            # Удаляем старые блюда
            instance.order_dishes.all().delete()
            # Добавляем новые блюда
            for item_data in items_data:
                OrderDish.objects.create(
                    order=instance,
                    dish=item_data['dish'],
                    quantity=item_data['quantity'],
                    price_at_order=item_data['price_at_order']
                )
            # Пересчитываем общую стоимость
            instance.calculate_total_price()

        instance.save()
        return instance
