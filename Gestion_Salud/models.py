from django.db import models
from django.contrib.auth.models import AbstractUser
from .fields import RutField
from .utils.rut import format_rut


class User(AbstractUser):
    
    #Modelo de usuario personalizado con RUT y datos adicionales.
    #Este es el modelo principal para autenticación y recuperación de contraseña.
    
    #ENUMS
    POSITION_CHOICES = [
        ('MEDICO', 'Médico'),
        ('ENFERMERA', 'Enfermera'),
        ('ADMINISTRATIVO', 'Administrativo'),
        ('OTRO', 'Otro'),
    ]
    
    # Campos nuevos (los que NO vienen por defecto)
    rut = RutField(unique=True)

    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")

    institutional_email = models.CharField(max_length=255, unique=True, verbose_name="Email Institucional")

    position = models.CharField(max_length=100, choices=POSITION_CHOICES, verbose_name="Cargo")

    # AbstractUser ya incluye:
    # username, password, first_name, last_name, email,
    # is_active, is_superuser, is_staff, date_joined, etc.

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        
    def __str__(self):
        return f"{self.username} ({self.rut})"
    
    def get_full_name(self):
        """Retorna nombre completo con apellidos"""
        return f"{self.first_name} {self.last_name}".strip()

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