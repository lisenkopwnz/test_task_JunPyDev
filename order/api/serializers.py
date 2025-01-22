from rest_framework import serializers
from order.models import Dish, OrderDish, Order


class DishSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Dish.
    Используется для представления данных о блюде.
    """
    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']


class OrderDishSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели OrderDish.
    Используется для представления данных о блюде в заказе.
    """
    dish = DishSerializer(read_only=True)

    class Meta:
        model = OrderDish
        fields = ['dish', 'quantity', 'price_at_order']


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    Используется для представления данных о заказе, включая список блюд и статус.
    """
    items = OrderDishSerializer(source='order_dishes', many=True, read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status']


class OrderDishCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели OrderDish.
    Используется для создания и обновления данных о блюде в заказе.
    """
    class Meta:
        model = OrderDish
        fields = ['dish', 'quantity', 'price_at_order']


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    Используется для создания и обновления данных о заказе, включая список блюд.
    """
    items = OrderDishCreateUpdateSerializer(source='order_dishes', many=True, required=False)

    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']

    def create(self, validated_data: dict) -> Order:
        """
        Создает новый заказ на основе переданных данных.

        :param validated_data: Валидированные данные для создания заказа.
        :return: Созданный объект Order.
        """
        items_data = validated_data.pop('order_dishes')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderDish.objects.create(
                order=order,
                dish=item_data['dish'],
                quantity=item_data['quantity'],
                price_at_order=item_data['price_at_order']
            )
        order.calculate_total_price()
        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        """
        Обновляет существующий заказ на основе переданных данных.

        :param instance: Объект Order, который нужно обновить.
        :param validated_data: Валидированные данные для обновления заказа.
        :return: Обновленный объект Order.
        """
        items_data = validated_data.pop('order_dishes', None)

        # Обновляю table_number, если оно передано
        if 'table_number' in validated_data:
            instance.table_number = validated_data['table_number']

        # Обновляю статус, если он передан
        if 'status' in validated_data:
            instance.status = validated_data['status']

        # Обновляем список блюд, если он передан
        if items_data is not None:
            # Удаляю старые блюда
            instance.order_dishes.all().delete()
            # Добавляею новые блюда
            for item_data in items_data:
                OrderDish.objects.create(
                    order=instance,
                    dish=item_data['dish'],
                    quantity=item_data['quantity'],
                    price_at_order=item_data['price_at_order']
                )
            # Общуая стоимость пересчитывается
            instance.calculate_total_price()

        instance.save()
        return instance
