from django.urls import path

from .views import CustomerAutocomplete, ExecutorAutocomplete, AddressAutocomplete, DeviceAutocomplete,\
    AttachmentDetails, AttachmentDelete, OrderUpdateAPIView,\
    OrderList, OrderDetails, OrderUpdate, \
    AddressCreateModal, AddressDetails, CustomerCreateModal, CustomerDetails, DeviceCreateModal,\
    ServicesList, ServicesFiler, ServiceDetails, ServiceUpdate, ServiceDelete

app_name = 'orders'

urlpatterns = [
    path('', OrderList.as_view(), name='orders_list'),
    path('<int:pk>/', OrderDetails.as_view(), name='order_details'),
    path('<int:pk>/update/', OrderUpdate.as_view(), name='order_update'),
    path('create/', OrderUpdate.as_view(), name='order_create'),

    path('address_create/', AddressCreateModal.as_view(), name='address_create'),
    path('address_details/<int:pk>/', AddressDetails.as_view(), name='address_details'),

    path('customer_create/', CustomerCreateModal.as_view(), name='customer_create'),
    path('customer_details/<int:pk>/', CustomerDetails.as_view(), name='customer_details'),

    path('device_create/', DeviceCreateModal.as_view(), name='device_create'),

    path('services_list/', ServicesList.as_view(), name='services_list'),
    path('services_filter/', ServicesFiler.as_view(), name='services_filter'),
    path('service_details/<int:pk>/', ServiceDetails.as_view(), name='service_details'),
    path('service_update/', ServiceUpdate.as_view(), name='service_update'),
    path('service_delete/', ServiceDelete.as_view(), name='service_delete'),

    path('customer_autocomplete/', CustomerAutocomplete.as_view(), name='customer_autocomplete'),
    path('executor_autocomplete/', ExecutorAutocomplete.as_view(), name='executor_autocomplete'),
    path('address_autocomplete/', AddressAutocomplete.as_view(), name='address_autocomplete'),
    path('devices_autocomplete/', DeviceAutocomplete.as_view(), name='device_autocomplete'),

    path('attachment/<int:pk>/', AttachmentDetails.as_view(), name='attachment_details'),
    path('attachment/<int:pk>/delete/', AttachmentDelete.as_view(), name='attachment_delete'),

    path('api/<int:order_id>/update/', OrderUpdateAPIView.as_view(), name='order_update_api'),
]
