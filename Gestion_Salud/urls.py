from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='root'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('recuperar-clave/', views.IdentityVerificationView.as_view(), name='password_reset_verification'),
    path('recuperar-clave/confirmar/', views.CompletePasswordResetView.as_view(), name='password_reset_confirm'),
    
    path('home/', views.HomeView.as_view(), name='home'),
    path('dashboard/medico/', views.DoctorHomeView.as_view(), name='doctor_home'),
    path('dashboard/enfermeria/', views.NurseHomeView.as_view(), name='nurse_home'),
    path('dashboard/admision/', views.SecretaryHomeView.as_view(), name='secretary_home'),
    
    path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/admision/', views.AdmisionView.as_view(), name='admision_create'),
    path('pacientes/editar/<int:pk>/', views.PacienteUpdateView.as_view(), name='paciente_update'),
    
    # Rutas Clínicas
    path('ficha/<int:pk>/evolucionar/', views.ClinicalObservationCreateView.as_view(), name='agregar_evolucion'),
    path('ficha/<int:pk>/traslado/', views.TrasladoUpdateView.as_view(), name='traslado_paciente'),

    # Rutas de Agendamiento
    path('citas/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('citas/nueva/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('citas/editar/<int:pk>/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path('mis-citas/', views.DoctorAppointmentListView.as_view(), name='doctor_appointment_list'),
]