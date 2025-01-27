from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from produto.models import Produto

class Pedido(models.Model):
    STATUS_CHOICES = (
        ('A', 'Aprovado'),
        ('C', 'Criado'),
        ('R', 'Reprovado'),
        ('P', 'Pendente'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    numero = models.CharField(max_length=20, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='C')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    in_game_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Pedido N. {self.numero} - {self.get_status_display()}'

    def calcular_total(self):
        total = sum(item.get_total_item() for item in self.itens.all())
        self.total = total
        self.save()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField()
    imagem = models.URLField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f'Item do {self.pedido.numero}: {self.produto.nome}'

    def get_total_item(self):
        return self.quantidade * self.preco

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'