from django.urls import path

from .views import CustomerList, CustomerDetails, CustomerUpdate, CustomerCreate,\
    AdditionalAddressesList, AdditionalAddressDetails, AdditionalAddressUpdate, AdditionalAddressCreate,\
    AdditionalAddressDelete


app_name = 'customers'

urlpatterns = [
    path('', CustomerList.as_view(), name='customers_list'),
    path('<int:pk>/', CustomerDetails.as_view(), name='customer_details'),
    path('<int:pk>/update/', CustomerUpdate.as_view(), name='customer_update'),
    path('create/', CustomerCreate.as_view(), name='customer_create'),

    path('<int:customer_pk>/addresses/', AdditionalAddressesList.as_view(), name='addresses_list'),
    path('<int:customer_pk>/addresses/<int:pk>/', AdditionalAddressDetails.as_view(), name='address_details'),
    path('<int:customer_pk>/addresses/<int:pk>/update/', AdditionalAddressUpdate.as_view(), name='address_update'),
    path('<int:customer_pk>/addresses/<int:pk>/delete/', AdditionalAddressDelete.as_view(), name='address_delete'),
    path('<int:customer_pk>/addresses/create/', AdditionalAddressCreate.as_view(), name='address_create'),

]
