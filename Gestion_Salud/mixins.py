from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages

class RoleRequiredMixin(AccessMixin):
    """
    Mixin para requerir un rol específico (cargo) para acceder a la vista.
    Define `allowed_roles` en la vista como una lista de strings.
    Ej: allowed_roles = ['MEDICO', 'ENFERMERA']
    """
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if not self.allowed_roles:
            # Si no se definen roles, asumimos que cualquiera autenticado pasa (o restringimos todo, mejor warning)
            return super().dispatch(request, *args, **kwargs)

        if request.user.position not in self.allowed_roles and not request.user.is_superuser:
            messages.error(request, "No tienes permisos para acceder a esta sección.")
            return redirect('home') # O a una página de 403
        
        return super().dispatch(request, *args, **kwargs)
