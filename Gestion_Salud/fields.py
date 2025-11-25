from django.db import models
from .utils.validators import validar_rut
from .utils.rut import clean_rut, format_rut

class RutField(models.CharField):
    """
    Campo personalizado para RUT chileno.
    Guarda el RUT con formato en la BD (XX.XXX.XXX-Y).
    Valida automáticamente el RUT antes de guardar.
    """
    description = "RUT chileno"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 12)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """Convierte el valor a su representación Python (con formato)"""
        if not value:
            return value
        # Limpiar, validar y formatear
        rut_limpio = clean_rut(value)
        validar_rut(rut_limpio)  # Validar antes de formatear
        return format_rut(rut_limpio)

    def get_prep_value(self, value):
        """Valor que se guarda en la BD (con formato)"""
        if not value:
            return value
        # Limpiar, validar y formatear
        rut_limpio = clean_rut(value)
        validar_rut(rut_limpio)  # Validar antes de guardar
        return format_rut(rut_limpio)

    def from_db_value(self, value, expression, connection):
        """Valor que Django entrega al cargar desde BD (con formato)"""
        if not value:
            return value
        return value  # Ya está formateado en la BD
