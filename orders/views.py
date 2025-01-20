from django.db.models import Prefetch
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, DeleteView

from orders.forms import OrderForm, OrderDishFormSet
from orders.models import Order, OrderDish, Dish


class OrderListView(ListView):
    """
        Представление для отображения списка заказов на главной странице.
    """
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_filters(self):
        """
            Возаращает параметры фильтрации из GET запроса.
        """
        return {
            'table_number': self.request.GET.get('table_number'),
            'status': self.request.GET.get('status'),
        }

    def get_queryset(self):
        """
            Возвращает queryset заказов с предварительной загрузкой связанных данных.

            Использует:
                - `prefetch_related` для загрузки связанных объектов OrderDish и Dish.
                - `only` для выбора только необходимых полей.

            Возвращает:
                QuerySet: Список заказов с предварительно загруженными данными о блюдах и их количестве.
        """
        filters = self.get_filters()

        orders = Order.objects.prefetch_related(
            Prefetch('order_dishes', queryset=OrderDish.objects.only('quantity', 'price_at_order', 'dish')),
            Prefetch('order_dishes__dish', queryset=Dish.objects.only('name', 'price')),
        ).only('id', 'table_number', 'status')

        if filters['table_number']:
            orders = orders.filter(table_number=filters['table_number'])
        if filters['status']:
            orders = orders.filter(status=filters['status'])

        return orders


class CreateOrder(CreateView):
    """
        Представление для создания заказа с возможностью добавления блюд.
    """
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('orders:order_list')

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


@method_decorator(require_POST, name='dispatch')
class DeleteOrder(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return JsonResponse({"status": "success", "message": "Order deleted successfully"})
        except Order.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Order not found"}, status=404)







