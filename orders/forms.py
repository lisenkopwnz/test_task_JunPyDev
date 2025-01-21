from django import forms
from django.forms import inlineformset_factory

from orders.models import Order, OrderDish


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number']

OrderDishFormSet = inlineformset_factory(
    Order,
    OrderDish,
    fields=['dish', 'quantity', 'price_at_order'],
    extra=1,
    can_delete=False,
)


