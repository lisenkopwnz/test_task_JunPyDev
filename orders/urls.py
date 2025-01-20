from django.urls import path

from orders.views import OrderListView

urlpatterns = [
    path('', OrderListView.as_view()),
]