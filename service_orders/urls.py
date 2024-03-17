from django.urls import path

from .views import ServiceOrderList, ServiceOrderDetails, ServiceOrderUpdate, ServiceOrderCreate,\
    CustomerDetails, AddressDetails, CustomerCreateModal, AddressCreateModal


app_name = 'service_orders'

urlpatterns = [
    path('', ServiceOrderList.as_view(), name='list'),
    path('<int:pk>/', ServiceOrderDetails.as_view(), name='details'),
    path('<int:pk>/update/', ServiceOrderUpdate.as_view(), name='update'),
    path('create/', ServiceOrderCreate.as_view(), name='create'),

    path('customer_create/', CustomerCreateModal.as_view(), name='customer_create'),
    path('customer_details/<int:pk>/', CustomerDetails.as_view(), name='customer_details'),

    path('address_create/', AddressCreateModal.as_view(), name='address_create'),
    path('address_details/<int:pk>/', AddressDetails.as_view(), name='address_details'),
]
