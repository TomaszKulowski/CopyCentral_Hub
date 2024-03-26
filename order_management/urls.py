from django.urls import path

from .views import OrdersList, ApplyFilters

app_name = 'order_management'

urlpatterns = [
    path('', OrdersList.as_view(), name='orders_list'),
    path('apply_filters/', ApplyFilters.as_view(), name='apply_filters'),
]
