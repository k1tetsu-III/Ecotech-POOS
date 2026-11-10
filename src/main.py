import logging

from persistencia.conexion import ERRORES_BD, ErrorConfiguracion
from persistencia.crear_bd import crear_tablas
from menu_usuario import solicitar_login, solicitar_registro, menu_privado
from menu_empleado import menu_empleado
from menu_departamento import menu_departamento
from menu_proyecto import menu_proyecto
from menu_registrotiempo import menu_registrotiempo

def preparar_base_de_datos():
    """Crea las tablas. Devuelve False si la base de datos no está disponible."""
    try:
        crear_tablas()
        return True
    except ErrorConfiguracion as error:
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
    print("5. Crear cuenta para un empleado")
    print("0. Salir")


def flujo_principal(usuario_actual):
    """Maneja el ciclo principal de menús del sistema."""
    rol = usuario_actual.get("rol")
    if rol == "empleado":
        return menu_privado(usuario_actual) == "0"
    if rol != "admin":
        raise PermissionError("El rol de la sesión no es válido.")

    menus = {
        1: menu_empleado,
        2: menu_departamento,
        3: menu_proyecto,
        4: menu_registrotiempo,
    }

    while True:
        mostrar_menu()
        opcion = solicitar_opcion(5)
        if opcion == 0:
            print("Programa finalizado.")
            return True
        elif opcion in menus:
            menus[opcion]()
        elif opcion == 5:
            solicitar_registro(usuario_actual)


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
        print(
            f"\nBienvenido/a, {usuario_actual['nombre_usuario']} "
            f"(Rol: {usuario_actual['rol']})"
        )
        
        # Los administradores gestionan los módulos; los empleados solo usan
        # las opciones privadas de su cuenta.
        salir = flujo_principal(usuario_actual)
        if salir:
            return
        print("Sesión cerrada.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido. Hasta luego.")