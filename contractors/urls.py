from django.urls import path

from .views import ContractorsList, ContractorDetails, ContractorUpdate, ContractorCreate


app_name = 'contractors'

urlpatterns = [
    path('', ContractorsList.as_view(), name='list'),
    path('<int:pk>/', ContractorDetails.as_view(), name='details'),
    path('<int:pk>/update', ContractorUpdate.as_view(), name='update'),
    path('create/', ContractorCreate.as_view(), name='create'),

]
