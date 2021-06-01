from django.db import models


class EnderecoDeEntrega(models.Model):
    CHOICES = (
        ('casa', 'CASA'),
        ('apt', 'APARTAMENTO')
    )
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=100)
    numero = models.CharField(null=True)
    tipo_de_endereco = models.CharField(max_length=20, choices=CHOICES)
    
    
    