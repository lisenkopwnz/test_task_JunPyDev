import pytest
from django.core.exceptions import ValidationError

from order.models import OrderDish, Dish


@pytest.mark.django_db
def test_dish_creation(dish):
    """Тест создания блюда."""
    assert dish.name == "Пицца"
    assert dish.price == 10.50
    assert str(dish) == "Пицца"


@pytest.mark.django_db
def test_order_creation(order):
    """Тест создания заказа."""
    assert order.table_number == 1
    assert order.status == "pending"
    assert str(order) == f"Заказ {order.pk} - Стол 1"


@pytest.mark.django_db
def test_order_dish_creation(order_dish):
    """Тест создания связи заказа и блюда."""
    assert order_dish.quantity == 2
    assert order_dish.price_at_order == 10.50
    assert str(order_dish) == f"Пицца x 2 в Заказе {order_dish.order.id}"


@pytest.mark.django_db
def test_order_total_price_calculation(order, dish):
    """Тест расчета общей стоимости заказа."""
    OrderDish.objects.create(order=order, dish=dish, quantity=2, price_at_order=10.50)
    order.calculate_total_price()
    assert order.total_price == 21.00


@pytest.mark.django_db
def test_dish_price_validation():
    """Тест валидации цены блюда."""
    with pytest.raises(ValidationError) as exc_info:
        dish = Dish(name="Блюдо с отрицательной ценой", price=-10.00)
        dish.full_clean()  # Вызов валидации

    # Проверка сообщения об ошибке
    assert "Цена не может быть меньше 0 руб." in str(exc_info.value)