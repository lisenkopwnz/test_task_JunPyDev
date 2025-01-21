from django.contrib import admin
from .models import Dish, Order, OrderDish


class OrderDishInline(admin.TabularInline):  # или admin.StackedInline для другого вида отображения
    model = OrderDish
    extra = 1  # Количество пустых форм для добавления новых блюд

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDishInline]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDish)
class OrderDishAdmin(admin.ModelAdmin):
    pass
