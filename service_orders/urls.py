from django.urls import path

from .views import ServiceOrderList, ServiceOrderDetails, ServiceOrderUpdate,\
    CustomerDetails, AddressDetails, CustomerCreateModal, AddressCreateModal, DeviceCreateModal,\
    ServicesFiler, ServiceDetails, ServicesList, ServiceUpdate, ServiceDelete


app_name = 'service_orders'

urlpatterns = [
    path('', ServiceOrderList.as_view(), name='list'),
    path('<int:pk>/', ServiceOrderDetails.as_view(), name='details'),
    path('<int:pk>/update/', ServiceOrderUpdate.as_view(), name='update'),
    path('create/', ServiceOrderUpdate.as_view(), name='create'),

    path('customer_create/', CustomerCreateModal.as_view(), name='customer_create'),
    path('customer_details/<int:pk>/', CustomerDetails.as_view(), name='customer_details'),

    path('address_create/', AddressCreateModal.as_view(), name='address_create'),
    path('address_details/<int:pk>/', AddressDetails.as_view(), name='address_details'),

    path('device_create/', DeviceCreateModal.as_view(), name='device_create'),

    path('services_list/', ServicesList.as_view(), name='services_list'),
    path('services_filter/', ServicesFiler.as_view(), name='services_filter'),
    path('service_details/<int:pk>/', ServiceDetails.as_view(), name='service_details'),
    path('service_update/', ServiceUpdate.as_view(), name='service_update'),
    path('service_delete/', ServiceDelete.as_view(), name='service_delete'),

]
