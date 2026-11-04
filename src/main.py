#Paso 5 · main.py coordina la demostración
from persistencia.crear_bd import crear_tablas
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

crear_tablas()
empleado = Empleado(nombre="Ana Pérez", correo="ana@ecotech.cl")

print("Antes:", empleado.id)
# None

EmpleadoDAO.insertar(empleado)

print("Después:", empleado.id)
# id generado por la BD


def preparar_base_de_datos():
    #Crea las tablas. Devuelve False si la base no está disponible.
    try:
        crear_tablas()
        return True
    except ErrorConfiguracion as error:
        print(f"Configuración incorrecta: {error}. Revise el archivo .env.")
    except ERRORES_BD:
        logging.getLogger("ecotech").exception("No se pudo preparar la base de datos")
        print("No fue posible conectar con la base de datos. "
              "Revise la configuración del archivo .env.")
    return False


def main():
    logging.basicConfig(
        filename="ecotech.log",
        level=logging.ERROR,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if not preparar_base_de_datos():
        return

    menus = {
        1: menu_empleado,
        2: menu_departamento,
        3: menu_proyecto,
        4: menu_registrotiempo,
    }
    while True:
        mostrar_menu()
        opcion = solicitar_opcion(4)
        if opcion == 0:
            print("Hasta luego.")
            return
        menus[opcion]()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")
 #cambiar y revisar todolo que esta arriba de este comentario

#Inicio del programa con login inmediato
from menu_usuario import solicitar_login, menu_privado

def main():
    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ") == "0":
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None # Terminar el acceso de esta sesión.
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")
if __name__ == "__main__":
    main()

#Demostración · comprobar CREATE + READ desde main.py / clase 5
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

empleado = Empleado(
    nombre="Ana Torres",
    correo="ana.torres@ecotech.cl"
)

EmpleadoDAO.insertar(empleado)

encontrado = EmpleadoDAO.buscar_por_id(empleado.id)
print("Encontrado:", encontrado)

print("Listado:")
for item in EmpleadoDAO.listar():
    print(item)

#
from dependencia.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

def registrar_empleado():
    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()

    empleado = Empleado(nombre, correo)

    try:
        EmpleadoDAO.insertar(empleado)
        print("Empleado registrado correctamente.")
    except Exception:
        print("No fue posible registrar el empleado.")



#
from menus.menu_empleado import menu_empleado
from menus.menu_proyecto import menu_proyecto
    
def main():
    while True:
        print("\n=== SISTEMA ===")
        print("1. Empleados")
        print("2. Proyectos")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_empleado()
        elif opcion == "2":
            menu_proyecto()
        elif opcion == "0":
            break

if __name__ == "__main__":
    main()
