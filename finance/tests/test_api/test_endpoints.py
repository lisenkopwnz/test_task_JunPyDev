import pytest
from rest_framework.test import APIClient
from finance.tests.conftest import setup_test_data


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_revenue_list(api_client, setup_test_data):
    """
    Тестирование API для получения списка выручки.
    """
    response = api_client.get('/finance/api_revenue_list/')

    assert response.status_code == 200

    data = response.json()
    assert len(data['results']) == 2
    assert data['results'][0]['total_revenue'] == '1000.00'
    assert data['results'][1]['total_revenue'] == '500.00'

@pytest.mark.django_db
def test_calculate_revenue(api_client, setup_test_data):
    """
    Тестирование API для расчета выручки за сегодняшнюю смену.
    """
    # Выполняем GET-запрос
    response = api_client.get('/finance/api_calculate_revenue/')

    assert response.status_code == 200

    data = response.json()
    assert 'total_revenue' in data
    assert data['total_revenue'] == 800.00

@pytest.mark.django_db
def test_close_shift(api_client, setup_test_data):
    """
    Тестирование API для закрытия смены и сохранения выручки.
    """
    response = api_client.post('/finance/api_close_shift/')

    assert response.status_code == 200

    data = response.json()
    assert 'date' in data
    assert 'total_revenue' in data
    assert data['total_revenue'] == 800.00