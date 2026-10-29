import logging

from menu_comun import solicitar_opcion
from menu_departamento import menu_departamento
from menu_empleado import menu_empleado
from menu_proyecto import menu_proyecto
from menu_registrotiempo import menu_registrotiempo
from persistencia.conexion import ERRORES_BD, ErrorConfiguracion
from persistencia.crear_bd import crear_tablas


def mostrar_menu():
    print("\n===== ECOTECH SOLUTIONS =====")
    print("1. Empleados")
    print("2. Departamentos")
    print("3. Proyectos")
    print("4. Registro de tiempo")
    print("0. Salir")


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