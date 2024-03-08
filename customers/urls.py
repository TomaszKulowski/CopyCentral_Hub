from django.urls import path

from .views import CustomerList, CustomerDetails, CustomerUpdate, CustomerCreate


app_name = 'customers'

urlpatterns = [
    path('', CustomerList.as_view(), name='list'),
    path('<int:pk>/', CustomerDetails.as_view(), name='details'),
    path('<int:pk>/update', CustomerUpdate.as_view(), name='update'),
    path('create/', CustomerCreate.as_view(), name='create'),

]
