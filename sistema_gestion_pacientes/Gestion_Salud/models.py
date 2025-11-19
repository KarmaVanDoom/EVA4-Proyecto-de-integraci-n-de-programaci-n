import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username

class HealthPersonal(models.Model):
    uuid = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='health_profile'
    )
    
    rut = models.CharField(max_length=12, help_text="Ej: 12.345.678-9")
    cargo = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True) 

    class Meta:
        verbose_name = 'Personal de Salud'
        verbose_name_plural = 'Personal de Salud'

    def __str__(self):
        return f"{self.cargo} - {self.rut}"