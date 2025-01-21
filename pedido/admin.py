from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]
    list_display = 'numero', 'status', 'criado_em', 'total'

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
