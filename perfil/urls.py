from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('user/register/', views.createUser, name='register'),
    path('user/logout/', views.logoutView, name='logout'),
]
