from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import ValidatePrice


class Dish(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[ValidatePrice()])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class StatusChoices(models.TextChoices):
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
        return f"Заказ {self.pk} - Стол {self.table_number}"

    def calculate_total_price(self):
        total = sum(item.price_at_order * item.quantity for item in self.order_dishes.all())
        self.total_price = total


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_dishes')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.dish.name} x {self.quantity} в Заказе {self.order.id}"


class Revenue(models.Model):
    date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Выручка за {self.date}: {self.total_revenue}"
