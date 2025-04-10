from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from perfil.views import MyLoginView, createUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produto.urls')),
    path('perfil/', include('perfil.urls')),
    path('pedido/', include('pedido.urls')),

    path('accounts/login/', MyLoginView.as_view(), name='account_login'),
    path('accounts/signup/', createUser, name='account_signup'),
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)