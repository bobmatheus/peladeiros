from django.urls import path
from . import views

app_name = 'reservas'
urlpatterns = [
    path('', views.home, name='home'),
    path('campos/', views.campos_list, name='campos_list'),
    path('campos/<int:campo_id>/', views.campo_detail, name='campo_detail'),
    path('checkout/<int:campo_id>/', views.reserva_checkout, name='reserva_checkout'),
    path('confirmada/<int:reserva_id>/', views.reserva_confirmada, name='reserva_confirmada'),
]