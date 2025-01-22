import pytest
from order.models import Order, OrderDish, Dish
from order.signals import update_order_total_price


@pytest.mark.django_db
def test_update_order_total_price_signal(order, dish):
    """Тест сигнала для обновления общей стоимости заказа."""
    order_dish = OrderDish.objects.create(order=order, dish=dish, quantity=2, price_at_order=10.50)
    order.refresh_from_db()
    assert order.total_price == 21.00

    order_dish.quantity = 3
    order_dish.save()
    order.refresh_from_db()
    assert order.total_price == 31.50

    order_dish.delete()
    order.refresh_from_db()
    assert order.total_price == 0.00