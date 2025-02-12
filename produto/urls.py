from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import index, ListaProdutos, static_view



app_name = 'produto'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('lista/<int:jogo_id>/', ListaProdutos.as_view(), name='lista'),
    path('lista/<int:jogo_id>/<slug:tipo>/', ListaProdutos.as_view(), name='lista-filtrada'),
    path('addtocart/', views.AddtoCart.as_view(), name='addtocart'),
    path('removefromcart/', views.RemoveFromCart.as_view(), name='removefromcart'),
    path('updatecart/', views.UpdateCart.as_view(), name='updatecart'),
    path('cart/', views.Cart.as_view(), name='cart'),

    path('<str:pagina>/', static_view, name="static_view"),
]
