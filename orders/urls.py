from django.urls import path

from .views import CustomerAutocomplete, ExecutorAutocomplete, AddressAutocomplete, DeviceAutocomplete
app_name = 'orders'

urlpatterns = [
    path('customer_autocomplete/', CustomerAutocomplete.as_view(), name='customer_autocomplete'),
    path('executor_autocomplete/', ExecutorAutocomplete.as_view(), name='executor_autocomplete'),
    path('address_autocomplete/', AddressAutocomplete.as_view(), name='address_autocomplete'),
    path('devices_autocomplete/', DeviceAutocomplete.as_view(), name='device_autocomplete'),
]
