from django.urls import path

from .views import ServiceOrderList, ServiceOrderDetails, ServiceOrderUpdate, ServiceOrderCreate


app_name = 'service_orders'

urlpatterns = [
    path('', ServiceOrderList.as_view(), name='list'),
    path('<int:pk>/', ServiceOrderDetails.as_view(), name='details'),
    path('<int:pk>/update/', ServiceOrderUpdate.as_view(), name='update'),
    path('create/', ServiceOrderCreate.as_view(), name='create'),

]
