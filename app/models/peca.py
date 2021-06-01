from django.db import models
from django.conf import settings


class Peca(models.Model):
    modelo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self) -> str:
        return self.modelo


class DemandaDePeca(models.Model):
    STATUS_CHOICES = (
        (True, "Aberto"),
        (False, "Fechado"),
    )
    descricao = models.ForeignKey("Peca", on_delete=models.CASCADE)
    endereco_de_entrega = models.TextField()
    informacoes_de_contato = models.CharField(max_length=100)
    anunciante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_de_finalizacao = models.BooleanField(choices=STATUS_CHOICES, default=True)

    def __str__(self) -> str:
        return self.informacoes_de_contato