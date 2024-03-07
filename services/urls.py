from django.urls import path

from .views import ServicesList, ServiceDetails, ServiceUpdate, ServiceCreate


app_name = 'services'

urlpatterns = [
    path('', ServicesList.as_view(), name='list'),
    path('<int:pk>/', ServiceDetails.as_view(), name='details'),
    path('<int:pk>/update', ServiceUpdate.as_view(), name='update'),
    path('create/', ServiceCreate.as_view(), name='create'),

]
