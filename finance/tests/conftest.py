import pytest
from django.utils import timezone

from finance.models import Revenue
from order.models import Order


@pytest.fixture
def setup_test_data():
    """
    Фикстура для создания тестовых данных.
    """
    today = timezone.now().date()

    # Создаём заказы
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

    # Создаём записи о выручке
    Revenue.objects.create(date=today, total_revenue=1000.00)
    Revenue.objects.create(
        date=today - timezone.timedelta(days=1),
        total_revenue=500.00
    )
