import re

def clean_rut(rut: str) -> str:
    #Elimina puntos, guión y deja solo cuerpo + dv.
    return re.sub(r"[^0-9kK]", "", rut).upper()


def format_rut(rut: str) -> str:
    #Formatea un RUT a XX.XXX.XXX-Y
    rut = clean_rut(rut)
    cuerpo = rut[:-1]
    dv = rut[-1]

    cuerpo = f"{int(cuerpo):,}".replace(",", ".")
    return f"{cuerpo}-{dv}"

    