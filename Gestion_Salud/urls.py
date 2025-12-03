from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('recuperar-clave/', views.IdentityVerificationView.as_view(), name='password_reset_verification'),
    path('recuperar-clave/confirmar/', views.CompletePasswordResetView.as_view(), name='password_reset_confirm'),
    
    path('home/', views.HomeView.as_view(), name='home'),
    path('dashboard/medico/', views.DoctorHomeView.as_view(), name='doctor_home'),
    path('dashboard/enfermeria/', views.NurseHomeView.as_view(), name='nurse_home'),
    path('dashboard/admision/', views.SecretaryHomeView.as_view(), name='secretary_home'),
    
    path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/nuevo/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/editar/<int:pk>/', views.PacienteUpdateView.as_view(), name='paciente_update'),
]