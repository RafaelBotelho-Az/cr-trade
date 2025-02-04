from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to='produto_imagens', blank=True, null=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    TIPO_CHOICES = (
        ('tipo1', 'Moedas'),
        ('tipo2', 'Serviços'),
        ('tipo3', 'Gold'),
        ('tipo4', 'Outros'),
    )

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        blank=False,
        null=False,
        default='tipo1', 
        verbose_name='Tipo'
    )
    nome = models.CharField(max_length=255, verbose_name='Nome')
    imagem = models.ImageField(upload_to='produto_imagens')
    preco_marketing = models.FloatField(default=0, verbose_name='Preço')
    preco_marketing_promo = models.FloatField(default=0, verbose_name='Preço Promo')



    def __str__(self):
        return self.nome