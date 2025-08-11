# main/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservas.urls', namespace='reservas')),
    path('conta/', include('usuarios.urls', namespace='usuarios')),
]