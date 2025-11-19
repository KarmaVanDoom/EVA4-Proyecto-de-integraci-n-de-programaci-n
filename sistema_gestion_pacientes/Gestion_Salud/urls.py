from django.urls import path
from .views import (
    CustomLoginView, 
    CustomLogoutView, 
    IdentityVerificationView, 
    CompletePasswordResetView,
    HomeView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('recuperar-clave/', IdentityVerificationView.as_view(), name='password_reset_verification'),
    path('recuperar-clave/confirmar/', CompletePasswordResetView.as_view(), name='password_reset_confirm'),
    path('', HomeView.as_view(), name='home'),
]