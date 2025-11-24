from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .forms import CustomLoginForm, IdentityVerificationForm, CustomSetPasswordForm, PacienteForm
from .models import CustomUser, Paciente


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
            user = get_object_or_404(CustomUser, id=user_id)
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

@method_decorator(never_cache, name='dispatch')
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'Gestion_Salud/dashboard/home.html'
    login_url = 'login'

@method_decorator(never_cache, name='dispatch')
class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'Gestion_Salud/pacientes/paciente_list.html'
    context_object_name = 'pacientes'
    login_url = 'login'

@method_decorator(never_cache, name='dispatch')
class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'Gestion_Salud/pacientes/paciente_form.html'
    success_url = reverse_lazy('paciente_list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, "Paciente ingresado correctamente.")
        return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'Gestion_Salud/pacientes/paciente_form.html'
    success_url = reverse_lazy('paciente_list')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, "Ficha del paciente actualizada.")
        return super().form_valid(form)