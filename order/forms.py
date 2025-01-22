from django import forms
from django.forms import inlineformset_factory
from order.models import Order, OrderDish, Dish


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


class DishForm(forms.ModelForm):
    """Форма для создания и редактирования блюда."""

    class Meta:
        model = Dish
        fields = ['name', 'price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }