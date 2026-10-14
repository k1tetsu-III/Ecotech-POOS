from dominio.empleado import Empleado
from menu_comun import operacion_segura, pedir, solicitar_opcion
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from utilidades import correo_valido, entero_positivo, texto_no_vacio


def mostrar_menu():
    print("\n--- EMPLEADOS ---")
    print("1. Registrar empleado")
    print("2. Listar empleados")
    print("3. Buscar empleado por ID")
    print("4. Buscar empleado por correo")
    print("5. Actualizar empleado")
    print("6. Eliminar empleado")
    print("0. Volver")


def _pedir_departamento(mensaje):
    #Pide un ID de departamento existente. Devuelve None si se deja vacío.
    while True:
        id_depto = pedir(mensaje, entero_positivo, "El departamento", vacio_ok=True)
        if id_depto is None:
            return None
        if DepartamentoDAO.buscar_por_id(id_depto) is not None:
            return id_depto
        print("  No existe un departamento con ese ID.")


@operacion_segura
def registrar_empleado():
    nombre = pedir("Nombre: ", texto_no_vacio, "El nombre")
    correo = pedir("Correo: ", correo_valido)
    departamento_id = _pedir_departamento("ID de departamento (Enter = ninguno): ")
    empleado = Empleado(nombre, correo, departamento_id)
    EmpleadoDAO.insertar(empleado)
    print(f"  Empleado registrado con ID {empleado.id}.")


@operacion_segura
def listar_empleados():
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("  No hay empleados registrados.")
    for empleado in empleados:
        print(" ", empleado)


@operacion_segura
def buscar_empleado():
    id_empleado = pedir("ID del empleado: ", entero_positivo, "El ID")
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    print(" ", empleado if empleado else "Empleado no encontrado.")


@operacion_segura
def buscar_empleado_por_correo():
    correo = pedir("Correo: ", correo_valido)
    empleado = EmpleadoDAO.buscar_por_correo(correo)
    print(" ", empleado if empleado else "Empleado no encontrado.")


@operacion_segura
def actualizar_empleado():
    id_empleado = pedir("ID del empleado a actualizar: ", entero_positivo, "El ID")
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado is None:
        print("  Empleado no encontrado.")
        return
    print(" ", empleado)
    print("  (Enter para mantener el valor actual)")
    nombre = pedir("Nuevo nombre: ", texto_no_vacio, "El nombre", vacio_ok=True)
    correo = pedir("Nuevo correo: ", correo_valido, vacio_ok=True)
    departamento_id = _pedir_departamento("Nuevo ID de departamento: ")
    if nombre is not None:
        empleado.nombre = nombre
    if correo is not None:
        empleado.correo = correo
    if departamento_id is not None:
        empleado.departamento_id = departamento_id
    if EmpleadoDAO.actualizar(empleado):
        print("  Empleado actualizado correctamente.")
    else:
        print("  Empleado no encontrado.")


@operacion_segura
def eliminar_empleado():
    id_empleado = pedir("ID del empleado a eliminar: ", entero_positivo, "El ID")
    if EmpleadoDAO.eliminar(id_empleado):
        print("  Empleado eliminado correctamente.")
    else:
        print("  Empleado no encontrado.")


def menu_empleado():
    acciones = {
        1: registrar_empleado,
        2: listar_empleados,
        3: buscar_empleado,
        4: buscar_empleado_por_correo,
        5: actualizar_empleado,
        6: eliminar_empleado,
    }
    while True:
        mostrar_menu()
        opcion = solicitar_opcion(6)
        if opcion == 0:
            return
        acciones[opcion]()
