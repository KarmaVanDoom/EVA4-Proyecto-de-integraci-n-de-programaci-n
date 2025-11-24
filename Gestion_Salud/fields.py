from django.db import models
from .utils.validators import validar_rut
from .utils.rut import clean_rut, format_rut 

class RutField(models.CharField):
    description = "RUT chileno"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 12)
        kwargs.setdefault("validators", [validar_rut])
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return value
        return format_rut(value)

    def get_prep_value(self, value):
        """Valor que se guarda en la BD."""
        if not value:
            return value
        return format_rut(value)

    def from_db_value(self, value, expression, connection):
        #Valor que Django entrega al cargar desde BD.
        if not value:
            return value
        return format_rut(value)
