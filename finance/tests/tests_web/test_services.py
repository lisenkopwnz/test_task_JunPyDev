import pytest
from django.utils import timezone

from finance.services import RevenueService
from order.models import Order


@pytest.fixture
def setup_orders():
    """
    Фикстура для создания тестовых данных.
    """
    today = timezone.now().date()
    Order.objects.create(
        table_number=1,
        total_price=500.00,
        status='paid',
        created_at=timezone.now()
    )
    Order.objects.create(
        table_number=2,
        total_price=300.00,
        status='paid',
        created_at=timezone.now()
    )


@pytest.mark.django_db
def test_calculate_total_revenue(setup_orders):
    """
    Проверяет расчёт общей выручки за сегодня.
    """
    total_revenue = RevenueService.calculate_total_revenue()
    assert total_revenue == 800.00  # 500 + 300


@pytest.mark.django_db
def test_close_shift_and_save_revenue(setup_orders):
    """
    Проверяет создание и обновление записи о выручке.
    """
    # Первое закрытие смены
    revenue_record = RevenueService.close_shift_and_save_revenue()
    assert revenue_record.total_revenue == 800.00

    # Второе закрытие смены (должно обновить существующую запись)
    Order.objects.create(
        table_number=3,
        total_price=200.00,
        status='paid',
        created_at=timezone.now()
    )
    updated_revenue_record = RevenueService.close_shift_and_save_revenue()
    assert updated_revenue_record.total_revenue == 1000.00  # 800 + 200