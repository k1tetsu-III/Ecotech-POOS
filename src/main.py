import logging
import sqlite3
import pymysql

from persistencia.conexion import obtener_motor
from persistencia.crear_bd import crear_tablas
from menus.menu_usuario import solicitar_login, menu_privado
from menus.menu_empleado import menu_empleado
from menus.menu_departamento import menu_departamento
from menus.menu_proyecto import menu_proyecto
from menus.menu_registrotiempo import menu_registrotiempo

# Definición de excepciones según el motor
ERRORES_BD = (sqlite3.Error, pymysql.MySQLError)


def preparar_base_de_datos():
    """Crea las tablas. Devuelve False si la base de datos no está disponible."""
    try:
        crear_tablas()
        return True
    except ValueError as error:
        print(f"Error de configuración: {error}. Revise el archivo .env.")
    except ERRORES_BD:
        logging.getLogger("ecotech").exception("No se pudo preparar la base de datos")
        print("No fue posible conectar con la base de datos. Revise el archivo .env.")
    return False


def solicitar_opcion(max_opcion):
    """Solicita y valida una opción numérica del menú."""
    try:
        opcion = int(input(f"Seleccione una opción (0-{max_opcion}): "))
        if 0 <= opcion <= max_opcion:
            return opcion
    except ValueError:
        pass
    print("Opción inválida.")
    return None


def mostrar_menu():
    print("\n=== SISTEMA ECOTECH ===")
    print("1. Menú Empleados")
    print("2. Menú Departamentos")
    print("3. Menú Proyectos")
    print("4. Menú Registros de Tiempo")
    print("0. Salir")


def flujo_principal():
    """Maneja el ciclo principal de menús del sistema."""
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
            print("Cerrando sesión...")
            break
        elif opcion in menus:
            menus[opcion]()


def main():
    logging.basicConfig(
        filename="ecotech.log",
        level=logging.ERROR,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if not preparar_base_de_datos():
        return

    # Autenticación al iniciar
    while True:
        print("\n--- INICIO DE SESIÓN ---")
        usuario_actual = solicitar_login()
        
        if usuario_actual is None:
            if input("Presione Enter para reintentar o '0' para salir del programa: ").strip() == "0":
                print("Programa finalizado.")
                return
            continue

        # Si el usuario se autentica correctamente
        print(f"\nBienvenido/a, {usuario_actual.nombre_usuario} (Rol: {usuario_actual.rol})")
        
        # Ejecuta el flujo según el diseño deseado
        flujo_principal()
        
        usuario_actual = None  # Cierre de sesión al terminar


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido. Hasta luego.")