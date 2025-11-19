from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, HealthPersonal

# Configuración para ver el Perfil de Salud dentro del mismo formulario de Usuario
class HealthPersonalInline(admin.StackedInline):
    model = HealthPersonal
    can_delete = False
    verbose_name_plural = 'Ficha de Personal de Salud'

class CustomUserAdmin(UserAdmin):
    inlines = (HealthPersonalInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_cargo')

    def get_cargo(self, obj):
        try:
            return obj.health_profile.cargo
        except:
            return "-"
    get_cargo.short_description = 'Cargo'

# Registramos los modelos
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(HealthPersonal)