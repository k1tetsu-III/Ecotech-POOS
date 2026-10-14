import functools
import logging

from persistencia.conexion import ERRORES_BD, ERRORES_INTEGRIDAD, ErrorConfiguracion

_registro = logging.getLogger("ecotech")


def pedir(mensaje, validador, *args, vacio_ok=False):
    #Pide un dato por teclado hasta que sea válido.

    #Si vacio_ok es True, una entrada vacía devuelve None (dato opcional).
    
    while True:
        texto = input(mensaje).strip()
        if vacio_ok and texto == "":
            return None
        try:
            return validador(texto, *args)
        except ValueError as error:
            print(f"  Dato no válido: {error}")


def solicitar_opcion(maximo):
    #Pide una opción numérica entre 0 y maximo.
    while True:
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("  Debe ingresar un número.")
            continue
        if opcion < 0 or opcion > maximo:
            print("  Opción fuera de rango.")
            continue
        return opcion


# ------------------------------------------------------- manejo de errores UI

def operacion_segura(funcion):
    #Ejecuta una acción de menú sin que un error cierre el programa.

    # ValueError: dato que no cumple las reglas del dominio.
    # ERRORES_INTEGRIDAD: duplicados o relaciones (clave foránea, UNIQUE).
    # ERRORES_BD: cualquier otro fallo de base de datos (conexión, SQL...).
    # usuario ve un mensaje seguro; el detalle técnico va a ecotech.log.
    
    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        try:
            return funcion(*args, **kwargs)
        except ValueError as error:
            print(f"  Dato no válido: {error}")
        except ErrorConfiguracion as error:
            _registro.exception("Configuración incorrecta")
            print(f"  Configuración de base de datos incorrecta: {error}")
        except ERRORES_INTEGRIDAD:
            _registro.exception("Violación de integridad")
            print("  No se pudo completar: el dato está duplicado o "
                  "está relacionado con otros registros.")
        except ERRORES_BD:
            _registro.exception("Error de base de datos")
            print("  No fue posible completar la operación con la base de datos.")
    return envoltura
