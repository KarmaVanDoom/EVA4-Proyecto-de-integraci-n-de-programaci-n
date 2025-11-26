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

# Modelo de Centros de Salud (Healthcare Centers)
class HealthcareCenter(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Centro")
    type = models.CharField(max_length=50, verbose_name="Tipo de Centro") # Ej: Hospital, Clínica
    is_public = models.BooleanField(default=True, verbose_name="¿Es Público?")
    region = models.CharField(max_length=100, verbose_name="Región")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

# Modelo del Paciente (Patients)
class Paciente(models.Model):
    rut = models.CharField(max_length=13, unique=True, help_text="Ej: 11.222.333-K")
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name_father = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    last_name_mother = models.CharField(max_length=100, blank=True, null=True, verbose_name="Apellido Materno")
    birth_date = models.DateField(verbose_name="Fecha de Nacimiento")
    institutional_email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Email Institucional")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name_father} ({self.rut})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name_father} {self.last_name_mother or ''}".strip()

# Historial del Paciente / Ficha Técnica (Patient Records)
class PatientRecord(models.Model):
    patient = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='records', verbose_name="Paciente")
    healthcare_center = models.ForeignKey(HealthcareCenter, on_delete=models.CASCADE, verbose_name="Centro de Salud")
    
    admission_date = models.DateField(verbose_name="Fecha de Ingreso")
    discharge_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Alta")
    discharge_details = models.TextField(null=True, blank=True, verbose_name="Detalles del Alta")
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_records')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_records')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-admission_date']

    def __str__(self):
        return f"Ficha {self.id} - {self.patient}"