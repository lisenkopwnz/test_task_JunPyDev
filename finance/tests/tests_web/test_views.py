import pytest
from django.urls import reverse
from finance.models import Revenue
from django.utils import timezone
from finance.tests.conftest import setup_test_data

@pytest.mark.django_db
def test_revenue_list_view(client, setup_test_data):
    """
    Проверяет, что представление возвращает корректный список выручки.
    """
    url = reverse('finance:revenue_list')
    response = client.get(url)

    assert response.status_code == 200
    assert b"1000.00" in response.content
    assert b"500.00" in response.content


@pytest.mark.django_db
def test_calculate_revenue_view(client, setup_test_data):
    """
    Проверяет, что представление корректно отображает выручку за сегодня.
    """
    url = reverse('finance:calculate_revenue')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_close_shift_view(client, setup_test_data):
    """
    Проверяет, что представление корректно закрывает смену и перенаправляет на страницу списка выручки.
    """
    url = reverse('finance:close_shift')
    response = client.post(url)

    assert response.status_code == 302  # Перенаправление
    assert response.url == reverse('finance:revenue_list')

    # Проверяем, что запись о выручке создана
    today = timezone.now().date()
    revenue_record = Revenue.objects.get(date=today)
    assert revenue_record.total_revenue == 800.00