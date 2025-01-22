from django import forms
from django.forms import inlineformset_factory
from orders.models import Order, OrderDish


class OrderForm(forms.ModelForm):
    """
    Форма для модели Order.
    Используется для создания и редактирования заказов.
    Поле `table_number` обязательно для заполнения.
    """
    class Meta:
        model = Order
        fields = ['table_number']


# FormSet для модели OrderDish
OrderDishFormSet = inlineformset_factory(
    Order,  # Родительская модель
    OrderDish,  # Дочерняя модель
    fields=['dish', 'quantity', 'price_at_order'],  # Поля, которые будут отображаться в форме
    extra=1,  # Количество дополнительных пустых форм для добавления новых блюд
    can_delete=False,  # Запрещаем удаление существующих записей через FormSet
)
