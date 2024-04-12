from django.urls import path

from .views import HistoryList

app_name = 'history'

urlpatterns = [
    path('', HistoryList.as_view(), name='list'),
]
