# servicios/permisos.py
# Control de acceso y verificación de roles para las funciones del sistema.

def exigir_sesion(sesion):
    """Verifica que la sesión sea válida y corresponda a un usuario autenticado."""
    if not isinstance(sesion, dict):
        raise PermissionError("Debe iniciar sesión para realizar esta acción.")

    if sesion.get("rol") not in ("admin", "empleado"):
        raise PermissionError("Acceso no permitido.")

    empleado_id = sesion.get("empleado_id")
    if type(empleado_id) is not int or empleado_id <= 0:
        raise PermissionError("La sesión actual no es válida.")

def exigir_admin(sesion):
    """Verifica que el usuario de la sesión tenga permisos de administrador."""
    exigir_sesion(sesion)
    if sesion.get("rol") != "admin":
        raise PermissionError("Acción restringida únicamente para administradores.")