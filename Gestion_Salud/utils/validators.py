from django.core.exceptions import ValidationError
from .rut import clean_rut

def validar_rut(rut):
    rut = clean_rut(rut)

    if len(rut) < 8:
        raise ValidationError("RUT incompleto")

    cuerpo = rut[:-1]
    dv = rut[-1]

    suma = 0
    multiplo = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1

    dv_esperado = 11 - (suma % 11)
    dv_esperado = "0" if dv_esperado == 11 else "K" if dv_esperado == 10 else str(dv_esperado)

    if dv != dv_esperado:
        raise ValidationError("RUT inválido")
