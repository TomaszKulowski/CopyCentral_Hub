from django.urls import path

from .views import DevicesList, DeviceDetails, DeviceUpdate, DeviceCreate

app_name = 'devices'

urlpatterns = [
    path('', DevicesList.as_view(), name='list'),
    path('<int:pk>/', DeviceDetails.as_view(), name='details'),
    path('<int:pk>/update/', DeviceUpdate.as_view(), name='update'),
    path('create/', DeviceCreate.as_view(), name='create'),
]
