from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Q
from .forms import CustomLoginForm, IdentityVerificationForm, CustomSetPasswordForm, PacienteForm, ClinicalObservationForm, TrasladoForm, PatientRecordForm, AppointmentForm
from .models import User, Paciente, PatientRecord, ClinicalObservation, HealthcareCenter, Appointment
from .mixins import RoleRequiredMixin
import django.utils.timezone

# --- AUTHENTICATION ---

class CustomLoginView(LoginView):
    template_name = 'Gestion_Salud/auth/login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True 
    def get_success_url(self):
        return reverse_lazy('home') 
    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = 'login'

class IdentityVerificationView(FormView):
    template_name = 'Gestion_Salud/auth/password_reset_verification.html'
    form_class = IdentityVerificationForm
    success_url = reverse_lazy('password_reset_confirm')
    def form_valid(self, form):
        user = form.verified_user
        self.request.session['reset_user_id'] = str(user.id)
        messages.success(self.request, "Identidad verificada correctamente.")
        return super().form_valid(form)

class CompletePasswordResetView(FormView):
    template_name = 'Gestion_Salud/auth/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('login')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.session.get('reset_user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            kwargs['user'] = user 
        return kwargs
    def dispatch(self, request, *args, **kwargs):
        if 'reset_user_id' not in request.session:
            messages.error(request, "Acceso denegado. Primero verifique su identidad.")
            return redirect('password_reset_verification')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        form.save()
        del self.request.session['reset_user_id']
        messages.success(self.request, "Contraseña actualizada exitosamente. Inicie sesión.")
        return super().form_valid(form)

# --- DASHBOARDS ---

@method_decorator(never_cache, name='dispatch')
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'Gestion_Salud/dashboard/home.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.position == 'MEDICO':
            return redirect('doctor_home')
        elif user.position == 'ENFERMERA':
            return redirect('nurse_home')
        elif user.position == 'ADMINISTRATIVO':
            return redirect('secretary_home')
        return super().get(request, *args, **kwargs)

@method_decorator(never_cache, name='dispatch')
class DoctorHomeView(RoleRequiredMixin, ListView):
    # Dashboard Médico: Lista pacientes activos asignados o generales
    model = PatientRecord
    template_name = 'Gestion_Salud/dashboard/doctor_home.html'
    context_object_name = 'records'
    allowed_roles = ['MEDICO']

    def get_queryset(self):
        # Mostrar pacientes activos (no dados de alta)
        # Idealmente filtrar por médico tratante si se asignó, o todos si es general
        return PatientRecord.objects.filter(
            ~Q(status='ALTA')
        ).order_by('-admission_date')

@method_decorator(never_cache, name='dispatch')
class NurseHomeView(RoleRequiredMixin, ListView):
    # Dashboard Enfermera: Monitoreo por áreas
    model = PatientRecord
    template_name = 'Gestion_Salud/dashboard/nurse_home.html'
    context_object_name = 'records'
    allowed_roles = ['ENFERMERA']

    def get_queryset(self):
        # Filtrar por área si viene en GET, sino mostrar todos los activos
        queryset = PatientRecord.objects.filter(~Q(status='ALTA')).order_by('area', '-admission_date')
        area_filter = self.request.GET.get('area')
        if area_filter:
            queryset = queryset.filter(area=area_filter)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['area_choices'] = PatientRecord.AREA_CHOICES
        context['current_area'] = self.request.GET.get('area', '')
        return context

@method_decorator(never_cache, name='dispatch')
class SecretaryHomeView(RoleRequiredMixin, TemplateView):
    # Dashboard Administrativo: Acciones rápidas
    template_name = 'Gestion_Salud/dashboard/secretary_home.html'
    allowed_roles = ['ADMINISTRATIVO']

# --- PACIENTES Y ADMISIÓN ---

@method_decorator(never_cache, name='dispatch')
class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'Gestion_Salud/pacientes/paciente_list.html'
    context_object_name = 'pacientes'
    login_url = 'login'

    def get_queryset(self):
        return Paciente.objects.prefetch_related('records', 'records__medico_tratante').all()

@method_decorator(never_cache, name='dispatch')
class AdmisionView(RoleRequiredMixin, CreateView):
    # Vista inteligente para Admisión (Administrativo)
    model = Paciente
    form_class = PacienteForm
    template_name = 'Gestion_Salud/pacientes/admision_form.html'
    allowed_roles = ['ADMINISTRATIVO']
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        # Verificar si el paciente ya existe por RUT (aunque el form lo valida, aquí manejamos la lógica de negocio)
        rut = form.cleaned_data.get('rut')
        try:
            paciente = Paciente.objects.get(rut=rut)
            # Paciente existe: Solo creamos ficha nueva
            messages.info(self.request, f"El paciente {paciente.full_name} ya existe. Creando nuevo ingreso.")
            return self.create_record(paciente)
        except Paciente.DoesNotExist:
            # Paciente nuevo: Guardamos paciente y creamos ficha
            self.object = form.save()
            messages.success(self.request, "Paciente registrado exitosamente.")
            return self.create_record(self.object)

    def create_record(self, paciente):
        # Crear ficha automática en "ESPERA" y "URGENCIAS" (o valores por defecto)
        # Buscamos un centro de salud por defecto (el primero que encontremos o uno fijo)
        centro = HealthcareCenter.objects.first() 
        
        PatientRecord.objects.create(
            patient=paciente,
            healthcare_center=centro,
            admission_date=django.utils.timezone.now().date(),
            area='URGENCIAS',
            status='ESPERA',
            created_by=self.request.user
        )
        messages.success(self.request, "Ficha de ingreso creada (Urgencias / En Espera).")
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        # Si el error es solo que el RUT ya existe, procedemos a crear la ficha igual
        rut = form.data.get('rut')
        if 'rut' in form.errors and Paciente.objects.filter(rut=rut).exists():
             paciente = Paciente.objects.get(rut=rut)
             messages.info(self.request, f"Paciente encontrado: {paciente.full_name}. Generando nuevo ingreso.")
             return self.create_record(paciente)
        
        return super().form_invalid(form)

# --- GESTIÓN CLÍNICA (MÉDICOS) ---

@method_decorator(never_cache, name='dispatch')
class ClinicalObservationCreateView(RoleRequiredMixin, CreateView):
    model = ClinicalObservation
    form_class = ClinicalObservationForm
    template_name = 'Gestion_Salud/pacientes/observation_form.html'
    allowed_roles = ['MEDICO'] 
    
    def get_success_url(self):
        return reverse_lazy('doctor_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['record'] = get_object_or_404(PatientRecord, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        record = get_object_or_404(PatientRecord, pk=self.kwargs['pk'])
        form.instance.record = record
        form.instance.author = self.request.user
        messages.success(self.request, "Evolución agregada correctamente.")
        return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
class TrasladoUpdateView(RoleRequiredMixin, UpdateView):
    # Vista para cambiar Área y Estado (Alta/Traslado)
    model = PatientRecord
    form_class = TrasladoForm
    template_name = 'Gestion_Salud/pacientes/traslado_form.html'
    allowed_roles = ['MEDICO']
    success_url = reverse_lazy('doctor_home')

    def form_valid(self, form):
        messages.success(self.request, "Estado del paciente actualizado.")
        return super().form_valid(form)

# --- VISTAS AUXILIARES ---
# Mantenemos las vistas de edición de paciente por compatibilidad
class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'Gestion_Salud/pacientes/paciente_form.html'
    success_url = reverse_lazy('paciente_list')

# --- AGENDAMIENTO (ADMINISTRATIVO) ---

@method_decorator(never_cache, name='dispatch')
class AppointmentListView(RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'Gestion_Salud/appointments/appointment_list.html'
    context_object_name = 'appointments'
    allowed_roles = ['ADMINISTRATIVO']

    def get_queryset(self):
        return Appointment.objects.select_related('patient', 'doctor').order_by('date', 'time')

@method_decorator(never_cache, name='dispatch')
class AppointmentCreateView(RoleRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'Gestion_Salud/appointments/appointment_form.html'
    allowed_roles = ['ADMINISTRATIVO']
    success_url = reverse_lazy('appointment_list')

    def form_valid(self, form):
        messages.success(self.request, "Cita agendada correctamente.")
        return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
class AppointmentUpdateView(RoleRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'Gestion_Salud/appointments/appointment_form.html'
    allowed_roles = ['ADMINISTRATIVO']
    success_url = reverse_lazy('appointment_list')

    def form_valid(self, form):
        messages.success(self.request, "Cita actualizada correctamente.")
        return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
class DoctorAppointmentListView(RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'Gestion_Salud/appointments/doctor_appointment_list.html'
    context_object_name = 'appointments'
    allowed_roles = ['MEDICO']

    def get_queryset(self):
        # Filtrar citas para el médico logueado
        return Appointment.objects.filter(doctor=self.request.user).select_related('patient').order_by('date', 'time')

