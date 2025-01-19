from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from orders.models import OrderDish


@receiver(post_save, sender=OrderDish)
@receiver(post_delete, sender=OrderDish)
def update_order_total_price(sender, instance, **kwargs):
    """
    Обновляет общую стоимость заказа при сохранении или удалении OrderDish.
    """
    order = instance.order
    order.calculate_total_price()
    order.save(update_fields=['total_price'])
