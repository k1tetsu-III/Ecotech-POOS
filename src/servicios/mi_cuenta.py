# mi_cuenta.py
# Permite a un usuario con sesión activa consultar sus registros de tiempo y actualizar sus propios datos.

from servicios.permisos import exigir_sesion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO

def mis_registros(sesion):
    """Devuelve los registros de tiempo asociados al empleado de la sesión actual."""
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(
        sesion["empleado_id"]
    )

def actualizar_mis_datos(sesion, nombre: str, correo: str, direccion=None, telefono=None):
    """Permite al usuario autenticado actualizar su propia información personal."""
    exigir_sesion(sesion)

    # 1. Buscar al empleado en la base de datos
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])

    if empleado is None:
        raise ValueError("Empleado no encontrado.")

    # 2. Actualizar los atributos proporcionados; los setters validan sus valores.
    empleado.nombre = nombre
    empleado.correo = correo
    if direccion is not None:
        empleado.direccion = direccion
    if telefono is not None:
        empleado.telefono = telefono

    # 3. Persistir en la base de datos
    return EmpleadoDAO.actualizar(empleado)