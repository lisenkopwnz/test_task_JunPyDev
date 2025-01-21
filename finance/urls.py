from django.urls import path

from finance.api.endpoints import ApiRevenueList, ApiCloseShiftView
from finance.views import RevenueList, CalculateRevenue, CloseShiftView

app_name = 'finance'

urlpatterns = [
    path('revenue_list/', RevenueList.as_view(), name='revenue_list'),
    path('calculate_revenue/', CalculateRevenue.as_view(), name='calculate_revenue'),
    path('close_shift/', CloseShiftView.as_view(), name='close_shift'),

    path('api_revenue_list/', ApiRevenueList.as_view(), name='api_revenue_list'),
    path('api_calculate_revenue/', CalculateRevenue.as_view(), name='api_calculate_revenue'),
    path('api_close_shift/', ApiCloseShiftView.as_view(), name='api_close_shift'),
]