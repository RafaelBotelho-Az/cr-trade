from django.urls import path
from . import views
from perfil.views import meus_pedidos, cancelar_pedido

app_name = 'perfil'

urlpatterns = [
    path('meus-pedidos/', meus_pedidos, name='meus_pedidos'),
    path('meus-pedidos/cancelar/<int:pedido_id>/', cancelar_pedido, name='cancelar_pedido'),
    path('user/register/', views.createUser, name='register'),
    path('user/logout/', views.logoutView, name='logout'),
]
