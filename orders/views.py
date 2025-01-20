from django.db.models import Prefetch
from django.views.generic import ListView

from orders.models import Order, OrderDish, Dish


class OrderListView(ListView):
    """
        Представление для отображения списка заказов на главной странице.
    """
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        """
            Возвращает queryset заказов с предварительной загрузкой связанных данных.

            Использует:
                - `prefetch_related` для загрузки связанных объектов OrderDish и Dish.
                - `only` для выбора только необходимых полей.

            Возвращает:
                QuerySet: Список заказов с предварительно загруженными данными о блюдах и их количестве.
        """
        orders = Order.objects.prefetch_related(
            Prefetch('order_dishes', queryset=OrderDish.objects.only('quantity', 'price_at_order', 'dish')),
            Prefetch('order_dishes__dish', queryset=Dish.objects.only('name', 'price')),
        ).only('id', 'table_number', 'status')
        return orders
