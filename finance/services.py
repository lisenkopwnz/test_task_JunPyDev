from finance.models import Revenue
from order.models import Order

from django.utils import timezone
from django.db.models import Sum, Q


class RevenueService:
    """
    Сервис для работы с выручкой.
    """

    @staticmethod
    def calculate_total_revenue() -> float:
        """
        Рассчитывает общую выручку за оплаченные заказы за сегодня.

        :return: Общая выручка за сегодня.
        """
        today = timezone.now().date()
        total_revenue = Order.objects.filter(
            Q(status='paid') | Q(status='ready'),  # Только оплаченные заказы
            created_at__date=today  # Заказы, созданные сегодня
        ).aggregate(total=Sum('total_price'))['total']

        return total_revenue or 0  # Если выручки нет, возвращаем 0

    @staticmethod
    def close_shift_and_save_revenue() -> Revenue:
        """
        Закрытие смены: расчет и сохранение выручки за сегодня.

        :return: Запись о выручке за сегодня.
        """
        today = timezone.now().date()
        total_revenue = RevenueService.calculate_total_revenue()

        # Создается запись о выручке за сегодня
        revenue_record, created = Revenue.objects.get_or_create(
            date=today,
            defaults={'total_revenue': total_revenue},
        )

        # Если запись уже существует, она обновляется
        if not created:
            revenue_record.total_revenue = total_revenue
            revenue_record.save()

        return revenue_record
