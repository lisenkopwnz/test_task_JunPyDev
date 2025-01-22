import pytest
from django.utils import timezone

from finance.models import Revenue


@pytest.mark.django_db
def test_create_revenue():
    """
    Проверяет, что запись о выручке создаётся корректно.
    """
    today = timezone.now().date()
    revenue = Revenue.objects.create(date=today, total_revenue=1000.50)

    assert revenue.date == today
    assert revenue.total_revenue == 1000.50
    assert str(revenue) == f"Выручка за {today}: 1000.50"