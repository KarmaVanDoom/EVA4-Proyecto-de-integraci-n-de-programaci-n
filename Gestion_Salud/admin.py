from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Paciente, Area


class CustomUserAdmin(UserAdmin):
    """
    Configuración personalizada del admin para el modelo User
    """
    list_display = ('username', 'rut', 'first_name', 'last_name', 'position', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'position')
    search_fields = ('username', 'rut', 'first_name', 'last_name', 'institutional_email')
    ordering = ('username',)
    
    # Agregar los campos personalizados al formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal Adicional', {
            'fields': ('rut', 'birth_date', 'institutional_email', 'position')
        }),
    )
    
    # Agregar los campos personalizados al formulario de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Personal Adicional', {
            'fields': ('rut', 'birth_date', 'institutional_email', 'position')
        }),
    )


# Configuración visual para el Admin de Pacientes 
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombres', 'apellidos', 'estado', 'area_asignada', 'prevision')
    list_filter = ('estado', 'area_asignada', 'prevision')
    search_fields = ('rut', 'nombres', 'apellidos')
    ordering = ('-fecha_ingreso',)


# Registramos todos los modelos
admin.site.register(User, CustomUserAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Area)