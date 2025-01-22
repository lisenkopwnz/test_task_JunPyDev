from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import ValidatePrice


class Dish(models.Model):
    """Модель блюда, которое можно заказать."""
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[ValidatePrice()])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """Возвращает строковое представление блюда (его название)."""
        return self.name


class Order(models.Model):
    """Модель заказа, связанного с конкретным столом."""
    class StatusChoices(models.TextChoices):
        """Статусы заказа."""
        PENDING = 'pending', _('В ожидании')
        READY = 'ready', _('Готово')
        PAID = 'paid', _('Оплачено')

    table_number = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dishes = models.ManyToManyField(Dish, through='OrderDish', related_name='orders')

    def __str__(self):
        """Возвращает строковое представление заказа."""
        return f"Заказ {self.pk} - Стол {self.table_number}"

    def calculate_total_price(self):
        """Пересчитывает общую стоимость заказа на основе блюд и их количества."""
        total = sum(item.price_at_order * item.quantity for item in self.order_dishes.all())
        self.total_price = total


class OrderDish(models.Model):
    """Промежуточная модель для связи заказа и блюда с указанием количества и цены."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_dishes')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, validators=[ValidatePrice()])

    def __str__(self):
        """Возвращает строковое представление связи заказа и блюда."""
        return f"{self.dish.name} x {self.quantity} в Заказе {self.order.id}"
