from django.urls import path

from .views import ServicesList, ServiceDetails, ServiceUpdate, ServiceCreate,\
    BrandsList, BrandDetails, BrandUpdate, BrandCreate,\
    ModelsList, ModelDetails, ModelUpdate, ModelCreate


app_name = 'services'

urlpatterns = [
    path('', ServicesList.as_view(), name='services_list'),
    path('<int:pk>/', ServiceDetails.as_view(), name='service_details'),
    path('<int:pk>/update/', ServiceUpdate.as_view(), name='service_update'),
    path('create/', ServiceCreate.as_view(), name='service_create'),

    path('brands/', BrandsList.as_view(), name='brands_list'),
    path('brands/<int:pk>/', BrandUpdate.as_view(), name='brand_update'),
    path('brands/<int:pk>/update/', BrandDetails.as_view(), name='brand_details'),
    path('brands/create/', BrandCreate.as_view(), name='brand_create'),

    path('models/', ModelsList.as_view(), name='models_list'),
    path('models/<int:pk>/', ModelUpdate.as_view(), name='model_update'),
    path('models/<int:pk>/update/', ModelDetails.as_view(), name='model_details'),
    path('models/create/', ModelCreate.as_view(), name='model_create'),
]
