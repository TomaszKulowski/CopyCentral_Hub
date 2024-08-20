from django.urls import path

from .views import CustomerAutocomplete, ExecutorAutocomplete, AddressAutocomplete, DeviceAutocomplete,\
    ServiceAutocomplete, AttachmentDetails, AttachmentDelete, OrderUpdateAPIView, SortNumberUpdateApiView,\
    OrderList, OrderDetails, OrderUpdate, \
    AddressCreateModal, AddressDetails, CustomerCreateModal, CustomerDetails, DeviceCreateModal,\
    ServicesFiler, ServiceDetails, \
    OrderServicesList, OrderServiceDetails, OrderServiceCreate, OrderServiceUpdate, OrderServiceDelete, \
    GetReportApiView, SendReportApiView


app_name = 'orders'

urlpatterns = [
    path('', OrderList.as_view(), name='orders_list'),
    path('<int:pk>/', OrderDetails.as_view(), name='order_details'),
    path('<int:pk>/update/', OrderUpdate.as_view(), name='order_update'),
    path('create/', OrderUpdate.as_view(), name='order_create'),

    path('customer_create/', CustomerCreateModal.as_view(), name='customer_create'),

    path('attachment/<int:pk>/', AttachmentDetails.as_view(), name='attachment_details'),
    path('attachment/<int:pk>/delete/', AttachmentDelete.as_view(), name='attachment_delete'),

    path('api/customer_autocomplete/', CustomerAutocomplete.as_view(), name='customer_autocomplete_api'),
    path('api/executor_autocomplete/', ExecutorAutocomplete.as_view(), name='executor_autocomplete_api'),
    path('api/address_autocomplete/', AddressAutocomplete.as_view(), name='address_autocomplete_api'),
    path('api/devices_autocomplete/', DeviceAutocomplete.as_view(), name='device_autocomplete_api'),
    path('api/services_autocomplete/', ServiceAutocomplete.as_view(), name='service_autocomplete_api'),

    path('api/<int:order_id>/order_update/', OrderUpdateAPIView.as_view(), name='order_update_api'),
    path('api/<int:order_id>/sort_number_update/', SortNumberUpdateApiView.as_view(), name='sort_number_update_api'),
    path('api/<int:order_id>/get_report/', GetReportApiView.as_view(), name='get_report_api'),
    path('api/<int:order_id>/send_report/', SendReportApiView.as_view(), name='send_report_api'),

    path('api/address_create/', AddressCreateModal.as_view(), name='address_create'),
    path('api/address_details/<int:pk>/', AddressDetails.as_view(), name='address_details'),
    path('api/customer_details/<int:pk>/', CustomerDetails.as_view(), name='customer_details'),
    path('api/device_create/', DeviceCreateModal.as_view(), name='device_create'),

    path('api/services_filter/', ServicesFiler.as_view(), name='services_filter_api'),
    path('api/service_details/<int:pk>/', ServiceDetails.as_view(), name='service_details_api'),

    path('api/order_services_list/', OrderServicesList.as_view(), name='order_services_list_api'),
    path('api/order_service_details/<int:pk>/', OrderServiceDetails.as_view(), name='order_service_details_api'),
    path('api/order_service_create/', OrderServiceCreate.as_view(), name='order_service_create_api'),
    path('api/order_service_update/<int:pk>/', OrderServiceUpdate.as_view(), name='order_service_update_api'),
    path('api/order_service_delete/', OrderServiceDelete.as_view(), name='order_service_delete_api'),

]
