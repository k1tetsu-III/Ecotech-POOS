from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.permisos import exigir_admin
from utilidades import entero_positivo


def crear_hash(clave):
    return Usuario.encriptar_clave(clave)


def registrar_usuario(sesion, empleado_id, nombre, clave):
    exigir_admin(sesion)
    empleado_id = entero_positivo(empleado_id, "El ID del empleado")
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("No existe un empleado con ese ID.")
    if UsuarioDAO.buscar_por_empleado_id(empleado_id) is not None:
        raise ValueError("El empleado ya tiene una cuenta.")

    nombre = Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre_usuario(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")
    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, empleado_id)
    return UsuarioDAO.insertar(usuario).id

def autenticar(nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None
    try:
        Usuario.validar_clave(clave)
    except (TypeError, ValueError):
        return None
    cuenta = UsuarioDAO.buscar_por_nombre_usuario(nombre)

    if cuenta is None:
        return None

    if not cuenta.verificar_password(clave):
        return None
    if not Usuario.es_hash_bcrypt(cuenta.password_hash):
        hash_anterior = cuenta.password_hash
        hash_nuevo = Usuario.encriptar_clave(clave)
        if not UsuarioDAO.actualizar_password_hash(
            cuenta.id, hash_anterior, hash_nuevo
        ):
            cuenta = UsuarioDAO.buscar_por_nombre_usuario(nombre)
            if cuenta is None or not cuenta.verificar_password(clave):
                return None

    return {
        "id": cuenta.id,
        "empleado_id": cuenta.empleado_id,
        "nombre_usuario": cuenta.nombre_usuario,
        "rol": cuenta.rol,
    }
