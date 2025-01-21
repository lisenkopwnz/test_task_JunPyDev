from django.views.generic import ListView

from finance.models import Revenue


class RevenueList(ListView):
    """
        Представление для отображения списка расчета выручки за каждую смену.
    """
    template_name = 'finance/revenue_list.html'
    context_object_name = 'revenue'

    def get_queryset(self):
        return Revenue.objects.all().order_by('-date')
