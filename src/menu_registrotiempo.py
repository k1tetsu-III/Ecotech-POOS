from datetime import date

from dominio.registrotiempo import RegistroTiempo
from menu_comun import operacion_segura, pedir, solicitar_opcion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registrotiempo_dao import RegistroTiempoDAO
from utilidades import entero_positivo, fecha_valida, horas_validas, texto_opcional


def mostrar_menu():
    print("\n--- REGISTRO DE TIEMPO ---")
    print("1. Registrar horas")
    print("2. Listar todos los registros")
    print("3. Listar registros de un empleado")
    print("4. Listar registros de un proyecto")
    print("5. Actualizar registro")
    print("6. Eliminar registro")
    print("0. Volver")


@operacion_segura
def registrar_horas():
    empleado_id = pedir("ID del empleado: ", entero_positivo, "El empleado")
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        print("  Empleado no encontrado.")
        return
    proyecto_id = pedir("ID del proyecto: ", entero_positivo, "El proyecto")
    if ProyectoDAO.buscar_por_id(proyecto_id) is None:
        print("  Proyecto no encontrado.")
        return
    fecha = pedir(f"Fecha AAAA-MM-DD (Enter = hoy {date.today()}): ",
                  fecha_valida, vacio_ok=True) or date.today()
    horas = pedir("Horas trabajadas: ", horas_validas)
    descripcion = pedir("Descripción (opcional): ", texto_opcional, "La descripción")
    registro = RegistroTiempo(empleado_id, proyecto_id, fecha, horas, descripcion)
    RegistroTiempoDAO.insertar(registro)
    print(f"  Registro creado con ID {registro.id}.")


def _mostrar(registros):
    if not registros:
        print("  No hay registros.")
    for registro in registros:
        print(" ", registro)
    if registros:
        print(f"  Total: {sum(r.horas for r in registros):.2f} h")


@operacion_segura
def listar_registros():
    _mostrar(RegistroTiempoDAO.listar())


@operacion_segura
def listar_por_empleado():
    id_empleado = pedir("ID del empleado: ", entero_positivo, "El empleado")
    _mostrar(RegistroTiempoDAO.listar_por_empleado(id_empleado))


@operacion_segura
def listar_por_proyecto():
    id_proyecto = pedir("ID del proyecto: ", entero_positivo, "El proyecto")
    _mostrar(RegistroTiempoDAO.listar_por_proyecto(id_proyecto))


@operacion_segura
def actualizar_registro():
    id_registro = pedir("ID del registro a actualizar: ", entero_positivo, "El ID")
    registro = RegistroTiempoDAO.buscar_por_id(id_registro)
    if registro is None:
        print("  Registro no encontrado.")
        return
    print(" ", registro)
    print("  (Enter para mantener el valor actual)")
    fecha = pedir("Nueva fecha AAAA-MM-DD: ", fecha_valida, vacio_ok=True)
    horas = pedir("Nuevas horas: ", horas_validas, vacio_ok=True)
    descripcion = pedir("Nueva descripción: ", texto_opcional, "La descripción", vacio_ok=True)
    if fecha is not None:
        registro.fecha = fecha
    if horas is not None:
        registro.horas = horas
    if descripcion is not None:
        registro.descripcion = descripcion
    if RegistroTiempoDAO.actualizar(registro):
        print("  Registro actualizado correctamente.")
    else:
        print("  Registro no encontrado.")


@operacion_segura
def eliminar_registro():
    id_registro = pedir("ID del registro a eliminar: ", entero_positivo, "El ID")
    if RegistroTiempoDAO.eliminar(id_registro):
        print("  Registro eliminado correctamente.")
    else:
        print("  Registro no encontrado.")


def menu_registrotiempo():
    acciones = {
        1: registrar_horas,
        2: listar_registros,
        3: listar_por_empleado,
        4: listar_por_proyecto,
        5: actualizar_registro,
        6: eliminar_registro,
    }
    while True:
        mostrar_menu()
        opcion = solicitar_opcion(6)
        if opcion == 0:
            return
        acciones[opcion]()
