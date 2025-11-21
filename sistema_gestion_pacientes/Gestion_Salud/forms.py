from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from .models import CustomUser, HealthPersonal
from .models import Paciente

#  Formulario de Login 
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ingrese su Usuario o RUT',
            'id': 'login_user'
        }),
        label="Usuario"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'login_pass'
        }),
        label="Contraseña"
    )

#  Formulario de Verificación  (Para recuperar clave)
class IdentityVerificationForm(forms.Form):
    username = forms.CharField(
        label="Usuario del Sistema",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    rut = forms.CharField(
        label="RUT (Con puntos y guion)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'})
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        rut_input = cleaned_data.get('rut')
        fecha_input = cleaned_data.get('fecha_nacimiento')

        if username and rut_input and fecha_input:
            try:
                user = CustomUser.objects.get(username=username)
                perfil = user.health_profile 
                
                # Comparamos los datos ingresados con los de la base de datos
                if perfil.rut != rut_input:
                    raise forms.ValidationError("El RUT ingresado no coincide con el usuario.")
                
                if perfil.fecha_nacimiento != fecha_input:
                    raise forms.ValidationError("La fecha de nacimiento no coincide.")
                
                # Si todo está bien, guardamos el usuario verificado para usarlo en la vista
                self.verified_user = user
                
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("El usuario ingresado no existe.")
            except HealthPersonal.DoesNotExist:
                raise forms.ValidationError("Este usuario no tiene ficha de personal de salud activa.")
        
        return cleaned_data

#  Formulario para Establecer Nueva Contraseña
class CustomSetPasswordForm(SetPasswordForm):
    pass


# Formulario para Crear y editar los pacientes
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['rut', 'nombres', 'apellidos', 'fecha_nacimiento', 'prevision', 'area_asignada', 'estado']
        
        # Bootstrap a cada campo
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prevision': forms.Select(attrs={'class': 'form-select'}),
            'area_asignada': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }