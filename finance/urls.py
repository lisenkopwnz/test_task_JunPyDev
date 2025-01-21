from django.urls import path

from finance.views import RevenueList

app_name = 'finance'

urlpatterns = [
    path('revenue_list/', RevenueList.as_view(), name='revenue_list'),
]