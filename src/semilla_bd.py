import os

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.usuario import Usuario
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.crear_bd import crear_tablas
from persistencia.usuario_dao import UsuarioDAO


def _obtener_departamento_semilla():
    for departamento in DepartamentoDAO.listar():
        if departamento.nombre == "Tecnología":
            print(f"Usando departamento existente: {departamento.nombre}")
            return departamento

    departamento = DepartamentoDAO.insertar(Departamento(nombre="Tecnología"))
    print(f"Departamento creado: {departamento.nombre} (ID: {departamento.id})")
    return departamento


def _asegurar_usuario_semilla(empleado, nombre_usuario, rol, variable_clave):
    existente = UsuarioDAO.buscar_por_nombre_usuario(nombre_usuario)
    if existente is not None:
        if existente.empleado_id != empleado.id or existente.rol != rol:
            raise ValueError(
                f"El usuario semilla '{nombre_usuario}' ya existe con otra "
                "asociación o rol; no se modificó."
            )
        print(f"Usuario '{nombre_usuario}' ya existe.")
        return existente

    cuenta_empleado = UsuarioDAO.buscar_por_empleado_id(empleado.id)
    if cuenta_empleado is not None:
        raise ValueError(
            f"El empleado {empleado.id} ya tiene la cuenta "
            f"'{cuenta_empleado.nombre_usuario}'; no se creó '{nombre_usuario}'."
        )

    clave = os.getenv(variable_clave)
    if not clave:
        raise ValueError(
            f"Configure la variable {variable_clave} para crear "
            f"el usuario semilla '{nombre_usuario}'."
        )

    usuario = Usuario(
        empleado_id=empleado.id,
        nombre_usuario=nombre_usuario,
        password_hash=Usuario.encriptar_clave(clave),
        rol=rol,
    )
    UsuarioDAO.insertar(usuario)
    print(f"Usuario '{nombre_usuario}' creado correctamente.")
    return usuario


def cargar_datos_semilla():
    print("--- Carga de Datos Semilla ---")
    crear_tablas()

    depto_demo = _obtener_departamento_semilla()

    # 2. Cargar Empleados
    datos_empleados = [
        {
            "nombre": "Ana Torres",
            "correo": "ana.torres@ecotech.cl",
            "direccion": "Av. Providencia 1234, Santiago",
            "telefono": "+56912345678",
        },
        {
            "nombre": "Carlos Mendoza",
            "correo": "carlos.mendoza@ecotech.cl",
            "direccion": "Calle Los Olivos 432, Santiago",
            "telefono": "+56987654321",
        },
    ]

    empleados_creados = []
    for datos in datos_empleados:
        existente = EmpleadoDAO.buscar_por_correo(datos["correo"])
        if existente is not None:
            print(f"Empleado ya existe: {datos['correo']}")
            empleados_creados.append(existente)
        else:
            empleado = Empleado(
                nombre=datos["nombre"],
                correo=datos["correo"],
                direccion=datos["direccion"],
                telefono=datos["telefono"],
                departamento_id=depto_demo.id,
            )
            EmpleadoDAO.insertar(empleado)
            empleados_creados.append(empleado)
            print(f"Empleado creado: {empleado.nombre} ({empleado.correo})")

    # 3. Crear cuentas de demostración sin sobrescribir cuentas existentes.
    if empleados_creados:
        _asegurar_usuario_semilla(
            empleados_creados[0],
            "admin",
            "admin",
            "ECOTECH_SEED_ADMIN_PASSWORD",
        )

        if len(empleados_creados) > 1:
            _asegurar_usuario_semilla(
                empleados_creados[1],
                "cmendoza",
                "empleado",
                "ECOTECH_SEED_EMPLOYEE_PASSWORD",
            )


if __name__ == "__main__":
    cargar_datos_semilla()
    print("Semilla ejecutada con éxito.")