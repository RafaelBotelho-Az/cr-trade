from django.contrib import admin
from .models import Pedido, ItemPedido


@admin.action(description="Marcar pedidos como finalizados")
def marcar_como_finalizado(modeladmin, request, queryset):
    queryset.update(status="F")


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline
    ]
    list_display = 'numero', 'status', 'criado_em', 'total', 'usuario'
    actions = [marcar_como_finalizado]

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
