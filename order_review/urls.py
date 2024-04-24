from django.urls import path

from .views import OrderReviewList
app_name = 'order_review'

urlpatterns = [
    path('', OrderReviewList.as_view(), name='orders_list'),
]
