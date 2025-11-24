from .rut import format_rut

class RutModelMixin:
    def save(self, *args, **kwargs):
        if hasattr(self, "rut") and self.rut:
            self.rut = format_rut(self.rut)
        super().save(*args, **kwargs)
