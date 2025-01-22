import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from order.models import Order, OrderDish, Dish


@pytest.mark.django_db
def test_api_order_update(client, order):
    """
    Тест обновления существующего заказа (API).
    """
    url = reverse('orders:api_order_update', args=[order.id])
    data = {
        'table_number': 3,
        'status': 'ready',
    }
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.table_number == 3
    assert order.status == 'ready'


@pytest.mark.django_db
def test_api_order_delete(client, order):
    """
    Тест удаления заказа (API).
    """
    url = reverse('orders:api_order_delete_api', args=[order.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_api_remove_dish_from_order(client, order_dish):
    """
    Тест удаления блюда из заказа (API).
    """
    order = order_dish.order
    dish = order_dish.dish
    url = reverse('orders:api_remove_dish_from_order', args=[order.id, dish.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert not OrderDish.objects.filter(order=order, dish=dish).exists()


# Тесты для DishViewSet
@pytest.mark.django_db
def test_dish_viewset_list(client, dish):
    """
    Тест получения списка блюд (API).
    """
    url = reverse('orders:dish-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['id'] == dish.id


@pytest.mark.django_db
def test_dish_viewset_create(client):
    """
    Тест создания нового блюда (API).
    """
    url = reverse('orders:dish-list')
    data = {
        'name': 'Суп',
        'price': 5.00,
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Dish.objects.count() == 1
    assert Dish.objects.first().name == 'Суп'


@pytest.mark.django_db
def test_dish_viewset_update(client, dish):
    """
    Тест обновления блюда (API).
    """
    url = reverse('orders:dish-detail', args=[dish.id])
    data = {
        'name': 'Пицца с грибами',
        'price': 12.00,
    }
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == 200
    dish.refresh_from_db()
    assert dish.name == 'Пицца с грибами'
    assert dish.price == 12.00


@pytest.mark.django_db
def test_dish_viewset_delete(client, dish):
    """
    Тест удаления блюда (API).
    """
    url = reverse('orders:dish-detail', args=[dish.id])
    response = client.delete(url)
    assert response.status_code == 204
    assert Dish.objects.count() == 0


# Тесты для веб-интерфейса
@pytest.mark.django_db
def test_order_list_view(client, order):
    """
    Тест отображения списка заказов (веб-интерфейс).
    """
    url = reverse('orders:order_list')
    response = client.get(url)
    assert response.status_code == 200
    assert str(order.id) in response.content.decode('utf-8')


@pytest.mark.django_db
def test_create_order_view(client):
    """
    Тест отображения страницы создания заказа (веб-интерфейс).
    """
    url = reverse('orders:create_order')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_order_view(client, order):
    """
    Тест удаления заказа (веб-интерфейс).
    """
    url = reverse('orders:delete_order', args=[order.id])
    response = client.post(url)
    assert response.status_code == 204
    assert not Order.objects.filter(pk=order.id).exists()


@pytest.mark.django_db
def test_update_order_status_view(client, order):
    """
    Тест обновления статуса заказа (веб-интерфейс).
    """
    url = reverse('orders:update_status', args=[order.id])
    response = client.post(url, {'status': 'ready'})
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.status == 'ready'


@pytest.mark.django_db
def test_menu_list_view(client, dish):
    """
    Тест отображения меню (веб-интерфейс).
    """
    url = reverse('orders:menu_list')
    response = client.get(url)
    assert response.status_code == 200
    assert dish.name in response.content.decode('utf-8')


@pytest.mark.django_db
def test_dish_delete_view(client, dish):
    """
    Тест удаления блюда (веб-интерфейс).
    """
    url = reverse('orders:delete_dish', args=[dish.id])
    response = client.post(url)
    assert response.status_code == 302  # Ожидаем редирект
    assert response.url == reverse('orders:menu_list')  # Проверяем URL редиректа
    assert not Dish.objects.filter(pk=dish.id).exists()


@pytest.mark.django_db
def test_dish_create_view(client):
    """
    Тест отображения страницы создания блюда (веб-интерфейс).
    """
    url = reverse('orders:create_dish')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_dish_update_view(client, dish):
    """
    Тест отображения страницы редактирования блюда (веб-интерфейс).
    """
    url = reverse('orders:update_dish', args=[dish.id])
    response = client.get(url)
    assert response.status_code == 200