from dominio.proyecto import Proyecto
from menu_comun import operacion_segura, pedir, solicitar_opcion
from persistencia.proyecto_dao import ProyectoDAO
from utilidades import entero_positivo, texto_no_vacio, texto_opcional


def mostrar_menu():
    print("\n--- PROYECTOS ---")
    print("1. Registrar proyecto")
    print("2. Listar proyectos")
    print("3. Buscar proyecto por ID")
    print("4. Actualizar proyecto")
    print("5. Eliminar proyecto")
    print("0. Volver")


@operacion_segura
def registrar_proyecto():
    nombre = pedir("Nombre del proyecto: ", texto_no_vacio, "El nombre")
    descripcion = pedir("Descripción (opcional): ", texto_opcional, "La descripción")
    proyecto = Proyecto(nombre, descripcion)
    ProyectoDAO.insertar(proyecto)
    print(f"  Proyecto registrado con ID {proyecto.id}.")


@operacion_segura
def listar_proyectos():
    proyectos = ProyectoDAO.listar()
    if not proyectos:
        print("  No hay proyectos registrados.")
    for proyecto in proyectos:
        print(" ", proyecto)


@operacion_segura
def buscar_proyecto():
    id_proyecto = pedir("ID del proyecto: ", entero_positivo, "El ID")
    proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
    print(" ", proyecto if proyecto else "Proyecto no encontrado.")


@operacion_segura
def actualizar_proyecto():
    id_proyecto = pedir("ID del proyecto a actualizar: ", entero_positivo, "El ID")
    proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
    if proyecto is None:
        print("  Proyecto no encontrado.")
        return
    print(" ", proyecto)
    print("  (Enter para mantener el valor actual)")
    nombre = pedir("Nuevo nombre: ", texto_no_vacio, "El nombre", vacio_ok=True)
    descripcion = pedir("Nueva descripción: ", texto_opcional, "La descripción", vacio_ok=True)
    if nombre is not None:
        proyecto.nombre = nombre
    if descripcion is not None:
        proyecto.descripcion = descripcion
    if ProyectoDAO.actualizar(proyecto):
        print("  Proyecto actualizado correctamente.")
    else:
        print("  Proyecto no encontrado.")


@operacion_segura
def eliminar_proyecto():
    id_proyecto = pedir("ID del proyecto a eliminar: ", entero_positivo, "El ID")
    if ProyectoDAO.eliminar(id_proyecto):
        print("  Proyecto eliminado correctamente.")
    else:
        print("  Proyecto no encontrado.")


def menu_proyecto():
    acciones = {
        1: registrar_proyecto,
        2: listar_proyectos,
        3: buscar_proyecto,
        4: actualizar_proyecto,
        5: eliminar_proyecto,
    }
    while True:
        mostrar_menu()
        opcion = solicitar_opcion(5)
        if opcion == 0:
            return
        acciones[opcion]()
