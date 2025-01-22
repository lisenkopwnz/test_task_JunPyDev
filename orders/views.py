import logging
from typing import Dict, Union, Any

from django.core.exceptions import ValidationError
from django.db.models import Prefetch, QuerySet
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView

from orders.forms import OrderForm, OrderDishFormSet
from orders.models import Order, OrderDish, Dish


logger = logging.getLogger(__name__)

class OrderListView(ListView):
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_filters(self) -> Dict[str, Union[str, str|None]]:
        """
        Возвращает параметры фильтрации из GET-запроса.
        """
        table_number = self.request.GET.get('table_number')
        status = self.request.GET.get('status')

        # Логируем некорректный номер стола, но не прерываем выполнение
        if table_number and not table_number.isdigit():
            logger.warning(f"Некорректный номер стола: {table_number}")
            table_number = None  # Игнорируем некорректное значение

        return {
            'table_number': table_number,
            'status': status,
        }

    def get_queryset(self) -> QuerySet[Order]:
        """
        Возвращает queryset заказов с предварительной загрузкой связанных данных.
        """
        try:
            filters = self.get_filters()
            orders = Order.objects.prefetch_related(
                Prefetch('order_dishes', queryset=OrderDish.objects.only('quantity', 'price_at_order', 'dish')),
                Prefetch('order_dishes__dish', queryset=Dish.objects.only('name', 'price')),
            ).only('id', 'table_number', 'status')

            if filters['table_number']:
                orders = orders.filter(table_number=int(filters['table_number']))
            if filters['status']:
                orders = orders.filter(status=filters['status'])

            return orders

        except Exception as e:
            # Логируем любую ошибку, но возвращаем пустой queryset
            logger.error(f"Ошибка при получении списка заказов: {e}")
            return Order.objects.none()


class CreateOrder(CreateView):
    """
    Представление для создания заказа с возможностью добавления блюд.
    """
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('orders:order_list')

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Добавляет OrderDishFormSet в контекст шаблона.

        Возвращает:
            Dict[str, Any]: Контекст данных для шаблона.
        """
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context_data['order_dish_formset'] = OrderDishFormSet(self.request.POST)
        else:
            context_data['order_dish_formset'] = OrderDishFormSet()
        return context_data

    def form_valid(self, form) -> Any:
        """
        Обрабатывает сохранение заказа и связанных блюд, если все данные валидны.

        Возвращает:
            HttpResponse: Результат обработки валидной формы.
        """
        context_data = self.get_context_data()
        order_dish_formset = context_data['order_dish_formset']

        try:
            if order_dish_formset.is_valid():
                # Сохраняем заказ
                self.object = form.save()

                # Связываем FormSet с созданным заказом
                order_dish_formset.instance = self.object

                # Сохраняем блюда
                order_dish_formset.save()
                return super().form_valid(form)
            else:
                # Если FormSet невалиден, логируем ошибки
                logger.warning(f"Ошибки в OrderDishFormSet: {order_dish_formset.errors}")
                return self.render_to_response(self.get_context_data(form=form))

        except ValidationError as e:
            # Логирую ошибки валидации
            logger.error(f"Ошибка валидации при создании заказа: {e}")
            return self.render_to_response(self.get_context_data(form=form))

        except Exception as e:
            # Логирую любую другую ошибку
            logger.error(f"Неожиданная ошибка при создании заказа: {e}")
            return self.render_to_response(self.get_context_data(form=form))


@method_decorator(require_POST, name='dispatch')
class DeleteOrder(View):
    """
        Обрабатывает POST-запросы для удаления заказа по его ID.

        Атрибуты:
            Нет атрибутов.

        Методы:
            post(request, *args, **kwargs):
                Удаляет заказ по ID и возвращает соответствующий HTTP-статус.

        Пример использования:
            URL: `order/delete_order/<int:pk>/`
            Метод: POST
        """
    def post(self, request: HttpRequest, *args: Any, **kwargs: Dict[str, Any]) -> HttpResponse:
        order_id = kwargs.get('pk')
        try:
            # Получаю заказ по ID
            order = Order.objects.get(id=order_id)
            order.delete()
            logger.info(f"Заказ {order_id} успешно удалён.")
            return HttpResponse(status=204)
        except Order.DoesNotExist:
            logger.error(f"Заказ {order_id} не найден.")
            return HttpResponse(status=404)
        except Exception as e:
            logger.error(f"Ошибка при удалении заказа {order_id}: {str(e)}")
            return HttpResponse(status=500)


class UpdateOrderStatus(View):
    """
    Класс для обновления статуса заказа.

    Метод `post` принимает запрос и идентификатор заказа, обновляет статус заказа
    на новый, если он предоставлен, и возвращает JSON-ответ с результатом операции.
    """

    def post(self, request: HttpRequest, order_id: int) -> JsonResponse:
        """
        Обрабатывает POST-запрос для обновления статуса заказа.

        :param request: HTTP-запрос.
        :param order_id: Идентификатор заказа.
        :return: JsonResponse с результатом операции.
        """
        try:
            # Получаем заказ по идентификатору или возвращаем 404, если заказ не найден
            order = get_object_or_404(Order, id=order_id)

            # Получаем новый статус из POST-запроса
            new_status = request.POST.get('status')

            if new_status:
                # Обновляем статус заказа и сохраняем его
                order.status = new_status
                order.save()

                logger.info(f"Статус заказа {order_id} успешно изменен на '{new_status}'.")

                return JsonResponse({'status': 'success', 'message': 'Статус успешно изменен.'})
            else:
                logger.error(f"Неверный статус для заказа {order_id}.")
                return JsonResponse({'status': 'error', 'message': 'Неверный статус.'}, status=400)

        except Exception as e:
            logger.error(f"Ошибка при обновлении статуса заказа {order_id}: {str(e)}")

            return JsonResponse({'status': 'error', 'message': 'Внутренняя ошибка сервера.'}, status=500)
