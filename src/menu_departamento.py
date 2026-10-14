from dominio.departamento import Departamento
from menu_comun import operacion_segura, pedir, solicitar_opcion
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from utilidades import entero_positivo, texto_no_vacio


def mostrar_menu():
    print("\n--- DEPARTAMENTOS ---")
    print("1. Registrar departamento")
    print("2. Listar departamentos")
    print("3. Ver empleados de un departamento")
    print("4. Actualizar departamento")
    print("5. Eliminar departamento")
    print("0. Volver")


@operacion_segura
def registrar_departamento():
    nombre = pedir("Nombre del departamento: ", texto_no_vacio, "El nombre")
    departamento = Departamento(nombre)
    DepartamentoDAO.insertar(departamento)
    print(f"  Departamento registrado con ID {departamento.id}.")


@operacion_segura
def listar_departamentos():
    departamentos = DepartamentoDAO.listar()
    if not departamentos:
        print("  No hay departamentos registrados.")
    for departamento in departamentos:
        print(" ", departamento)


@operacion_segura
def ver_empleados_departamento():
    id_depto = pedir("ID del departamento: ", entero_positivo, "El ID")
    departamento = DepartamentoDAO.buscar_por_id(id_depto)
    if departamento is None:
        print("  Departamento no encontrado.")
        return
    # Se reconstruye la relación UML 1 ---- 0..* con objetos, no con textos.
    for empleado in EmpleadoDAO.listar_por_departamento(departamento.id):
        departamento.agregar_empleado(empleado)
    print(" ", departamento)
    for empleado in departamento.empleados:
        print("   -", empleado)


@operacion_segura
def actualizar_departamento():
    id_depto = pedir("ID del departamento a actualizar: ", entero_positivo, "El ID")
    departamento = DepartamentoDAO.buscar_por_id(id_depto)
    if departamento is None:
        print("  Departamento no encontrado.")
        return
    print(" ", departamento)
    departamento.nombre = pedir("Nuevo nombre: ", texto_no_vacio, "El nombre")
    if DepartamentoDAO.actualizar(departamento):
        print("  Departamento actualizado correctamente.")
    else:
        print("  Departamento no encontrado.")


@operacion_segura
def eliminar_departamento():
    id_depto = pedir("ID del departamento a eliminar: ", entero_positivo, "El ID")
    if DepartamentoDAO.eliminar(id_depto):
        print("  Departamento eliminado (sus empleados quedan sin departamento).")
    else:
        print("  Departamento no encontrado.")


def menu_departamento():
    acciones = {
        1: registrar_departamento,
        2: listar_departamentos,
        3: ver_empleados_departamento,
        4: actualizar_departamento,
        5: eliminar_departamento,
    }
    while True:
        mostrar_menu()
        opcion = solicitar_opcion(5)
        if opcion == 0:
            return
        acciones[opcion]()
