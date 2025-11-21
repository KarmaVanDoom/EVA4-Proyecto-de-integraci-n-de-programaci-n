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

#  Modelos para las Áreas del Hospital UCI, Urgencias, y esas cosas
class Area(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

#  Modelo del Paciente
class Paciente(models.Model):
    # Opciones para listas desplegables 
    PREVISION_CHOICES = [
        ('FONASA', 'Fonasa'),
        ('ISAPRE', 'Isapre'),
        ('PARTICULAR', 'Particular'),
    ]

    ESTADO_CHOICES = [
        ('ESPERA', 'En Sala de Espera'),
        ('TRATAMIENTO', 'En Tratamiento'),
        ('UCI', 'En UCI / Crítico'),
        ('ALTA', 'Dada de Alta'),
    ]

    # Datos Personales
    rut = models.CharField(max_length=12, unique=True, help_text="Ej: 11.222.333-K")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    # Datos Clínicos
    prevision = models.CharField(max_length=20, choices=PREVISION_CHOICES, default='FONASA')
    area_asignada = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Área Asignada")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ESPERA')
    
    # Auditoría Cuándo llegó
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_ingreso'] # Los más nuevos primero

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.rut})"