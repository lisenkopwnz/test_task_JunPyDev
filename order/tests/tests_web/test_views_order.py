import pytest
from django.urls import reverse
from order.models import Order, Dish


@pytest.mark.django_db
def test_order_list_view(client):
    """Тест отображения списка заказов."""
    url = reverse('orders:order_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_order_view(client):
    """Тест создания заказа."""
    url = reverse('orders:create_order')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_order_view(client, order):
    """Тест удаления заказа."""
    url = reverse('orders:delete_order', args=[order.pk])
    response = client.post(url)
    assert response.status_code == 204
    assert not Order.objects.filter(pk=order.pk).exists()


@pytest.mark.django_db
def test_update_order_status_view(client, order):
    """Тест обновления статуса заказа."""
    url = reverse('orders:update_status', args=[order.pk])
    response = client.post(url, {'status': 'ready'})
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.status == 'ready'


@pytest.mark.django_db
def test_menu_list_view(client, dish):
    """Тест отображения меню."""
    url = reverse('orders:menu_list')
    response = client.get(url)
    assert response.status_code == 200
    assert dish.name in response.content.decode('utf-8')
