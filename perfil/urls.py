from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('user/register', views.createUser, name='register'),
    # path('user/login/', views.Login.as_view(), name='login'),
    # path('user/logout/', views.Logout.as_view(), name='logout'),
]
