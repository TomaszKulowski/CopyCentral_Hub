from django.urls import path

from .views import LoginView, LogoutView


app_name = 'authentication'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('sign_up/', LogoutView.as_view(), name='contractor_sing_up'),
]
