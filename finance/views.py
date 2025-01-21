from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from finance.models import Revenue
from finance.services import calculate_total_revenue, close_shift_and_save_revenue


class RevenueList(ListView):
    """
        Представление для отображения списка расчета выручки за каждую смену.
    """
    template_name = 'finance/revenue_list.html'
    context_object_name = 'revenue'

    def get_queryset(self):
        return Revenue.objects.all().order_by('-date')

class CalculateRevenue(View):
    """
    Представление для расчета выручки за сегодняшнюю смену.
    """
    template_name = 'finance/calculate_revenue.html'

    def get(self, request):
        # Получаем текущую дату
        today = timezone.now().date()

        # Рассчитываем общую выручку за оплаченные заказы за сегодня
        total_revenue = calculate_total_revenue()

        context = {
            'total_revenue': total_revenue,
        }
        return render(request, self.template_name, context)


class CloseShiftView(View):
    """
    Представление для закрытия смены и сохранения выручки за сегодня.
    """
    def post(self, request):

        close_shift_and_save_revenue()

        return redirect('finance:revenue_list')  # Перенаправляем на страницу списка выручки