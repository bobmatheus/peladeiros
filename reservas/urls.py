# reservas/urls.py
from django.urls import path
from .views_public import (
    HomeView, CamposListView, CampoDetailView,
    DisponibilidadeHX, ReservaCheckoutView, ReservaConfirmacaoView
)

app_name = 'reservas'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('campos/', CamposListView.as_view(), name='campos_list'),
    path('campos/<int:campo_id>/', CampoDetailView.as_view(), name='campo_detail'),
    path('hx/disponibilidade/', DisponibilidadeHX.as_view(), name='hx_disponibilidade'),
    path('reservar/', ReservaCheckoutView.as_view(), name='checkout'),
    path('confirmacao/', ReservaConfirmacaoView.as_view(), name='confirmacao'),
]