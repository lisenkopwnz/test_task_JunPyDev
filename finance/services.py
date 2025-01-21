from django.db.models import Sum
from django.utils import timezone

from finance.models import Revenue
from orders.models import Order


def calculate_total_revenue():
    # Получаем текущую дату
    today = timezone.now().date()

    # Рассчитываем общую выручку за оплаченные заказы за сегодня
    total_revenue = Order.objects.filter(
        status='paid',  # Только оплаченные заказы
        created_at__date=today  # Заказы, созданные сегодня
    ).aggregate(total=Sum('total_price'))['total']

    return total_revenue or 0  # Если выручки нет, возвращаем 0

def close_shift_and_save_revenue():
    """
    Закрытие смены: расчет и сохранение выручки за сегодня.
    """
    # Получаем текущую дату
    today = timezone.now().date()

    # Рассчитываем общую выручку за оплаченные заказы за сегодня
    total_revenue = Order.objects.filter(
        status='paid',  # Только оплаченные заказы
        created_at__date=today  # Заказы, созданные сегодня
    ).aggregate(total=Sum('total_price'))['total']

    total_revenue = total_revenue or 0  # Если выручки нет, устанавливаем 0

    # Создаем запись о выручке за сегодня
    revenue_record, created = Revenue.objects.get_or_create(
        date=today,
        defaults={'total_revenue': total_revenue},
    )

    # Если запись уже существует, обновляем её
    if not created:
        revenue_record.total_revenue = total_revenue
        revenue_record.save()

    return revenue_record