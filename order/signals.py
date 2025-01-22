from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Model

from order.models import OrderDish


@receiver(post_save, sender=OrderDish)
@receiver(post_delete, sender=OrderDish)
def update_order_total_price(sender: Model, instance: OrderDish, **kwargs) -> None:
    """
    Обновляет общую стоимость заказа при сохранении или удалении OrderDish.

    Аргументы:
        sender (Model): Модель, которая отправила сигнал (OrderDish).
        instance (OrderDish): Экземпляр модели OrderDish, который был сохранен или удален.
        **kwargs: Дополнительные аргументы, передаваемые сигналом.
    """
    order = instance.order
    order.calculate_total_price()
    order.save(update_fields=['total_price'])
