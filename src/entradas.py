# entradas.py
# Función auxiliar reutilizable para solicitar y validar entradas de usuario por consola.

def pedir_dato(mensaje: str, validador, leer=None):
    """
    Solicita una entrada por consola y aplica una función de validación.
    Reintenta automáticamente si se lanza TypeError o ValueError.
    """
    if leer is None:
        leer = input

    while True:
        entrada = leer(mensaje)
        try:
            return validador(entrada)
        except (TypeError, ValueError) as error:
            print(f"Error: {error} Intente nuevamente.\n")

pedir = pedir_dato
