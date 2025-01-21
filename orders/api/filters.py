import django_filters

from orders.models import Order


class OrderFilter(django_filters.FilterSet):
    table_number = django_filters.NumberFilter(field_name='table_number')
    status = django_filters.CharFilter(field_name='status')

    class Meta:
        model = Order
        fields = ['table_number', 'status']