from django.contrib import admin
from .models import Produto, Categoria

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco_marketing', 'preco_marketing_promo', 'categoria']

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)