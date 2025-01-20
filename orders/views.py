from lib2to3.fixes.fix_input import context

from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from orders.forms import OrderForm, OrderDishFormSet
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


class CreateOrder(CreateView):
    """
        Представление для создания заказа с возможностью добавления блюд.
    """
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('create_order')

    def get_context_data(self, **kwargs):
        """
            Добавляет OrderDishFormSet в контекст шаблона.
        """
        context_data = super().get_context_data(**kwargs)
        # Если данные отправлены через POST, инициализируем FormSet
        if self.request.method == 'POST':
            context_data['order_dish_formset'] = OrderDishFormSet(self.request.POST)
        else:
            # Иначе создаем пустой
            context_data['order_dish_formset'] = OrderDishFormSet()
        return context_data

    def form_valid(self, form):
        """
        Обрабатывает сохранение заказа и связанных блюд, если все данные валидны.
        """
        context_data = self.get_context_data()
        order_dish_formset = context_data['order_dish_formset']

        # Проверяем валидность FormSet
        if order_dish_formset.is_valid():
            self.object = form.save()

            # Связываем FormSet с созданным заказом
            order_dish_formset.instance = self.object

            # Сохраняем блюда
            order_dish_formset.save()
            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form))










