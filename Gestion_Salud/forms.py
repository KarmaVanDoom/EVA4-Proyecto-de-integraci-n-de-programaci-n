from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from .models import User, Paciente
from .utils.rut import clean_rut, format_rut
from .utils.validators import validar_rut
from django.core.exceptions import ValidationError

#  Formulario de Login 
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ingrese su Usuario o RUT',
            'id': 'id_username'
        }),
        label="Usuario o RUT"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'login_pass'
        }),
        label="Contraseña"
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Si parece un RUT (contiene números y guión o puntos), intentamos limpiarlo y formatearlo
        if any(char.isdigit() for char in username):
            try:
                rut_limpio = clean_rut(username)
                # Intentar validar el RUT
                validar_rut(rut_limpio)
                rut_formateado = format_rut(rut_limpio)
                # Buscar usuario por RUT formateado
                try:
                    user = User.objects.get(rut=rut_formateado)
                    return user.username  # Retornamos el username para el proceso de autenticación
                except User.DoesNotExist:
                    pass  # Si no existe, continuar con el username original
            except ValidationError:
                pass  # Si el RUT no es válido, continuar con el username original
        
        return username

#  Formulario de Verificación  (Para recuperar clave)
class IdentityVerificationForm(forms.Form):
    username = forms.CharField(
        label="Usuario del Sistema",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    rut = forms.CharField(
        label="RUT (Con puntos y guion)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9', 'id': 'id_rut'})
    )
    fecha_nacimiento = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    def clean_rut(self):
        rut_input = self.cleaned_data.get('rut')
        if rut_input:
            try:
                rut_limpio = clean_rut(rut_input)
                validar_rut(rut_limpio)
                return format_rut(rut_limpio)  # Retornar con formato para comparar
            except ValidationError as e:
                raise forms.ValidationError(str(e))
        return rut_input

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        rut_input = cleaned_data.get('rut')
        fecha_input = cleaned_data.get('fecha_nacimiento')

        if username and rut_input and fecha_input:
            try:
                user = User.objects.get(username=username)
                
                # Comparamos los datos ingresados con los de la base de datos (RUT con formato)
                if user.rut != rut_input:
                    raise forms.ValidationError("El RUT ingresado no coincide con el usuario.")
                
                if user.birth_date != fecha_input:
                    raise forms.ValidationError("La fecha de nacimiento no coincide.")
                
                # Si todo está bien, guardamos el usuario verificado para usarlo en la vista
                self.verified_user = user
                
            except User.DoesNotExist:
                raise forms.ValidationError("El usuario ingresado no existe.")
        
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
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9', 'id': 'id_rut'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prevision': forms.Select(attrs={'class': 'form-select'}),
            'area_asignada': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            try:
                rut_limpio = clean_rut(rut)
                validar_rut(rut_limpio)
                return format_rut(rut_limpio)  # Retornar con formato
            except ValidationError as e:
                raise forms.ValidationError(str(e))
        return rut

