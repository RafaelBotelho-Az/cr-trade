from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario.first_name} {self.usuario.last_name}' 
    
    def clean(self):
        pass

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'