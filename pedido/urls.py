from django.urls import path
from .views import criar_pedido, detalhe_pedido

app_name = 'pedido'

urlpatterns = [
    path('criar/', criar_pedido, name='criar'),
    path('detalhe/<int:pk>/', detalhe_pedido, name='detalhe'),
]