from django.contrib import admin
from .models import Dish, Order, OrderDish


class OrderDishInline(admin.TabularInline):
    """
    Inline-админка для модели OrderDish.
    Позволяет редактировать блюда в заказе  на странице заказа.
    """
    model = OrderDish
    extra = 1  # Количество пустых форм для добавления новых блюд


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админка для модели Order.
    Включает inline-формы для редактирования связанных блюд (OrderDish).
    """
    inlines = [OrderDishInline]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """
    Админка для модели Dish.
    Позволяет управлять блюдами через административную панель.
    """
    pass  # Используем стандартные настройки админки


@admin.register(OrderDish)
class OrderDishAdmin(admin.ModelAdmin):
    """
    Админка для модели OrderDish.
    Позволяет управлять связями между заказами и блюдами через административную панель.
    """
    pass
