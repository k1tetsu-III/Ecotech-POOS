# gestion_empleados.py
# Administrar empleados requiere autorización de administrador

from servicios.permisos import exigir_admin
from persistencia.empleado_dao import EmpleadoDAO
from dominio.empleado import Empleado

def listar_todos(sesion):
    """Lista todos los empleados registrados (solo admin)."""
    exigir_admin(sesion)
    return EmpleadoDAO.listar()

def buscar_por_id(sesion, id_empleado: int):
    """Busca un empleado por su ID (solo admin)."""
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(id_empleado)

def crear_empleado(sesion, nombre: str, correo: str, direccion=None, telefono=None, departamento_id=None):
    """Crea un nuevo empleado en la base de datos (solo admin)."""
    exigir_admin(sesion)
    # Instancia y valida la entidad en el dominio
    nuevo_empleado = Empleado(
        nombre=nombre,
        correo=correo,
        direccion=direccion,
        telefono=telefono,
        departamento_id=departamento_id
    )
    return EmpleadoDAO.insertar(nuevo_empleado)

def actualizar_empleado(sesion, id_empleado: int, nombre: str, correo: str, direccion=None, telefono=None, departamento_id=None):
    """Actualiza la información de un empleado existente (solo admin)."""
    exigir_admin(sesion)
    empleado = Empleado(
        nombre=nombre,
        correo=correo,
        direccion=direccion,
        telefono=telefono,
        departamento_id=departamento_id,
        id=id_empleado
    )
    return EmpleadoDAO.actualizar(empleado)

def eliminar_empleado(sesion, id_empleado: int):
    """Elimina un empleado si no posee registros de tiempo asociados (solo admin)."""
    exigir_admin(sesion)
    return EmpleadoDAO.eliminar(id_empleado)