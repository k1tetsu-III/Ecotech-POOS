import logging
from getpass import getpass

from dominio.usuario import Usuario
from entradas import pedir_dato
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.conexion import ERRORES_BD, ErrorConfiguracion
from servicios.autenticacion import autenticar, registrar_usuario
from servicios.permisos import exigir_admin
from servicios.servicios_api import ServicioExternoAPI
from utilidades import entero_positivo

_registro = logging.getLogger("ecotech")


def solicitar_registro(usuario_actual):
    exigir_admin(usuario_actual)
    try:
        empleado_id = pedir_dato(
            "ID del empleado: ",
            lambda valor: entero_positivo(valor, "El ID del empleado"),
        )
        empleado = EmpleadoDAO.buscar_por_id(empleado_id)
        if empleado is None:
            print("No existe un empleado con ese ID.")
            return None

        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)

        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None

        usuario_id = registrar_usuario(usuario_actual, empleado_id, nombre, clave)
    except ErrorConfiguracion as error:
        _registro.exception("Configuración incorrecta durante el registro")
        print(f"Configuración de base de datos incorrecta: {error}")
        return None
    except ERRORES_BD:
        _registro.exception("Error de base de datos durante el registro")
        print("No fue posible crear la cuenta por un problema con la base de datos.")
        return None
    except (TypeError, ValueError) as error:
        print(error)
        return None
    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except ErrorConfiguracion as error:
        _registro.exception("Configuración incorrecta durante el inicio de sesión")
        print(f"Configuración de base de datos incorrecta: {error}")
        return None
    except ERRORES_BD:
        _registro.exception("Error de base de datos durante el inicio de sesión")
        print("No fue posible iniciar sesión por un problema con la base de datos.")
        return None
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario

#Opciones protegidas por la sesión
def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['empleado_id']}")

def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    try:
        valor = ServicioExternoAPI.obtener_indicador_economico("dolar")
    except ErrorConfiguracion as error:
        _registro.exception("Configuración incorrecta al consultar indicador")
        print(f"Configuración de base de datos incorrecta: {error}")
    except ERRORES_BD:
        _registro.exception("Error de base de datos al guardar indicador")
        print("No fue posible guardar el indicador en la base de datos.")
    except RuntimeError as error:
        _registro.exception("No se pudo consultar el indicador externo")
        print(error)
    else:
        print(f"Valor del dólar: {valor}")

#Menú disponible después del login
def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    while True:
        print("1 Perfil, 2 Indicador, 9 Cerrar sesión, 0 Salir")
        opcion = input("Opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            mostrar_perfil(usuario_actual)
        elif opcion == "2":
            consultar_indicador(usuario_actual)
        else:
            print("Opción no válida.")