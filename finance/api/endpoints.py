from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from finance.api.pagination import RevenuePagination
from finance.api.serializers import RevenueSerializer
from finance.models import Revenue
from finance.services import RevenueService


class ApiRevenueList(ListAPIView):
    """
       API для получения списка записей о выручке.

       Этот API-метод позволяет получить список всех записей о выручке,
       отсортированных по дате в порядке убывания (от самой новой к самой старой).
       Данные возвращаются с пагинацией.

       Параметры:
       - `page` (int): Номер страницы для пагинации (по умолчанию 1).
       - `page_size` (int): Количество записей на странице (по умолчанию 15, максимум 20).

       Пример запроса:
       GET /finance/api_revenue_list/?page=2&page_size=10

       Пример ответа:
       {
           "count": 25,
           "next": "http://example.com/finance/api_revenue_list/?page=3&page_size=10",
           "previous": "http://example.com/finance/api_revenue_list/?page=1&page_size=10",
           "results": [
               {
                   "id": 1,
                   "date": "2023-10-01",
                   "total_revenue": "1000.00"
               },
               {
                   "id": 2,
                   "date": "2023-09-30",
                   "total_revenue": "500.00"
               }
           ]
       }
       """
    queryset = Revenue.objects.all().order_by('-date')
    serializer_class = RevenueSerializer
    pagination_class = RevenuePagination


class CalculateRevenueAPI(APIView):
    """
    API-метод для расчета выручки за сегодняшнюю смену.

    Этот API-метод возвращает общую выручку за сегодняшнюю смену.

    Пример запроса:
    GET /finance/api_calculate_revenue/

    Пример успешного ответа:
    {
        "total_revenue": 1500.00
    }

    Возможные ошибки:
    - 400: Некорректные данные (например, ошибка валидации).
    - 500: Внутренняя ошибка сервера.
    """

    def get(self, request):
        try:
            # Получаем общую выручку за сегодня
            total_revenue = RevenueService.calculate_total_revenue()

            return Response({
                'total_revenue': total_revenue
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'error': 'Ошибка валидации',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': 'Внутренняя ошибка сервера',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiCloseShift(APIView):
    """
    API для закрытия смены и сохранения выручки за сегодня.

    Этот API-метод закрывает текущую смену и сохраняет общую выручку за сегодня.
    Возвращает информацию о закрытой смене.

    Пример запроса:
    POST /finance/api_close_shift/

    Пример успешного ответа:
    {
        "date": "2023-10-05",
        "total_revenue": 1500.00
    }

    Возможные ошибки:
    - 400: Некорректные данные (например, ошибка валидации).
    - 500: Внутренняя ошибка сервера.
    """

    def post(self, request):
        try:
            # выручка сохраняется после закрытия смены
            revenue_record = RevenueService.close_shift_and_save_revenue()

            return Response({
                'date': revenue_record.date,
                'total_revenue': revenue_record.total_revenue,
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'error': 'Ошибка валидации',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': 'Внутренняя ошибка сервера',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
