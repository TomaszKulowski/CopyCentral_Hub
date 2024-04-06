from django.urls import path

from .views import OrdersList, ApplyFilters, EmployeesOrdersList, RegionsOrdersList

app_name = 'order_management'

urlpatterns = [
    path('', OrdersList.as_view(), name='orders_list'),
    path('employees/', EmployeesOrdersList.as_view(), name='employees_orders_list'),
    path('regions/', RegionsOrdersList.as_view(), name='regions_orders_list'),
    path('apply_filters/', ApplyFilters.as_view(), name='apply_filters'),
]
