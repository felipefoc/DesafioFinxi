from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    administrador = models.BooleanField(default=False)
    anunciante = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Usuario'