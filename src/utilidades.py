import re
from datetime import date, datetime

_PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ---------------------------------------------------------------- validadores
# Reciben el valor (normalmente un texto escrito por el usuario), lo validan
# y lo devuelven ya normalizado. Si no es válido lanzan ValueError.

def texto_no_vacio(valor, campo="El texto", maximo=100):
    if not isinstance(valor, str):
        raise ValueError(f"{campo} debe ser texto.")
    valor = valor.strip()
    if not valor:
        raise ValueError(f"{campo} no puede estar vacío.")
    if len(valor) > maximo:
        raise ValueError(f"{campo} no puede superar los {maximo} caracteres.")
    return valor


def texto_opcional(valor, campo="El texto", maximo=255):
    if valor is None or not str(valor).strip():
        return ""
    return texto_no_vacio(valor, campo, maximo)


def correo_valido(valor):
    correo = texto_no_vacio(valor, "El correo", 150).lower()
    if not _PATRON_CORREO.match(correo):
        raise ValueError("El correo no tiene un formato válido (ej: ana@ecotech.cl).")
    return correo


def entero_positivo(valor, campo="El valor"):
    if isinstance(valor, bool):
        raise ValueError(f"{campo} debe ser un número entero.")
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{campo} debe ser un número entero.") from None
    if numero <= 0:
        raise ValueError(f"{campo} debe ser mayor que cero.")
    return numero


def horas_validas(valor):
    try:
        horas = float(str(valor).replace(",", "."))
    except (TypeError, ValueError):
        raise ValueError("Las horas deben ser un número (ej: 2.5).") from None
    if not 0 < horas <= 24:
        raise ValueError("Las horas deben estar entre 0 y 24.")
    return round(horas, 2)


def fecha_valida(valor):
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    try:
        return datetime.strptime(str(valor).strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("La fecha debe tener formato AAAA-MM-DD (ej: 2026-10-07).") from None
