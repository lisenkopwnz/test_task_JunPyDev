from django.urls import path

from finance.views import RevenueList, CalculateRevenue, CloseShiftView

app_name = 'finance'

urlpatterns = [
    path('revenue_list/', RevenueList.as_view(), name='revenue_list'),
    path('calculate_revenue/', CalculateRevenue.as_view(), name='calculate_revenue'),
    path('close_shift/', CloseShiftView.as_view(), name='close_shift')
]