from django.db import models
from app.models import Produto

class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    produto_favorito = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.nome} ({self.email})'