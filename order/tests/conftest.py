import pytest
from order.models import Dish, Order, OrderDish


@pytest.fixture
def dish():
    """Фикстура для создания блюда."""
    return Dish.objects.create(name="Пицца", price=10.50)


@pytest.fixture
def order():
    """Фикстура для создания заказа."""
    return Order.objects.create(table_number=1)


@pytest.fixture
def order_dish(order, dish):
    """Фикстура для создания связи заказа и блюда."""
    return OrderDish.objects.create(order=order, dish=dish, quantity=2, price_at_order=10.50)