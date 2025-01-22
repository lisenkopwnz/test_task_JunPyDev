from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from finance.api.pagination import RevenuePagination
from finance.api.serializers import RevenueSerializer
from finance.models import Revenue
from finance.services import RevenueService


class ApiRevenueList(ListAPIView):
    queryset = Revenue.objects.all().order_by('-date')
    serializer_class = RevenueSerializer
    pagination_class = RevenuePagination

class CalculateRevenueAPIView(APIView):
    """
    API-метод для расчета выручки за сегодняшнюю смену.
    """

    def get(self, request):
        # Получаем общую выручку за сегодня
        total_revenue = RevenueService.calculate_total_revenue()

        # Возвращаем ответ с выручкой
        return Response({
            'total_revenue': total_revenue
        }, status=status.HTTP_200_OK)

class ApiCloseShiftView(APIView):

    """
    API для закрытия смены и сохранения выручки за сегодня.
    """
    def post(self, request):
        # Закрываем смену и сохраняем выручку
        revenue_record = RevenueService.close_shift_and_save_revenue()

        # Возвращаем информацию о закрытой смене
        return Response({
            'date': revenue_record.date,
            'total_revenue': revenue_record.total_revenue,
        }, status=status.HTTP_200_OK)