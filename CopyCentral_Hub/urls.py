"""
URL configuration for CopyCentral_Hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),

    path('authentication/', include('authentication.urls')),
    path('devices/', include('devices.urls')),
    path('customers/', include('customers.urls')),
    path('services/', include('services.urls')),
    path('orders/', include('orders.urls')),
    path('order_management/', include('order_management.urls')),
    path('history/', include('history.urls')),
    path("__debug__/", include("debug_toolbar.urls")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
