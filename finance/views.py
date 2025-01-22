import logging
from typing import Any, Dict
from urllib.request import Request

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from finance.models import Revenue
from finance.services import RevenueService

logger = logging.getLogger(__name__)

class RevenueList(ListView):
    """
    Представление для отображения списка выручки за каждую смену.

    Атрибуты:
        template_name (str): Имя шаблона для отображения списка выручки.
        context_object_name (str): Имя переменной контекста для списка выручки.
    """

    template_name: str = 'finance/revenue_list.html'
    context_object_name: str = 'revenue'

    def get_queryset(self) -> Any:
        """
        Возвращает отсортированный по дате список выручки.

        :return: QuerySet объектов Revenue, отсортированных по дате в обратном порядке.
        """
        return Revenue.objects.all().order_by('-date')

class CalculateRevenue(View):
    """
    Представление для расчета выручки за сегодняшнюю смену.

    Атрибуты:
        template_name (str): Имя шаблона для отображения страницы расчета выручки.
    """

    template_name: str = 'finance/calculate_revenue.html'

    def get(self, request: Any) -> Any:
        """
        Обрабатывает GET-запрос для расчета выручки за сегодня.

        :param request: HTTP-запрос.
        :return: HTTP-ответ с отрендеренным шаблоном и контекстом.
        """
        try:
            # Рассчитываем общую выручку за оплаченные заказы за сегодня
            total_revenue: float = RevenueService.calculate_total_revenue()

            context: Dict[str, Any] = {
                'total_revenue': total_revenue,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.error(f"Ошибка при расчете выручки: {str(e)}")
            return render(request, self.template_name, {'error': 'Произошла ошибка при расчете выручки.'})


class CloseShift(View):
    """
    Представление для закрытия смены и сохранения выручки за сегодня.
    """
    def post(self, request: Request)-> HttpResponse:
        try:
            RevenueService.close_shift_and_save_revenue()
            return redirect('finance:revenue_list')
        except Exception as e:
            logger.error(f"Ошибка при закрытии смены: {str(e)}")
            return render(request, 'finance/error.html',
                          {'error': 'Произошла ошибка при закрытии смены.'})
