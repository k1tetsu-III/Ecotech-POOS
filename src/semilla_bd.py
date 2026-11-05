from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.usuario import Usuario
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO


def cargar_datos_semilla():
    print("--- Carga de Datos Semilla ---")

    # 1. Cargar Departamento de prueba
    deptos = DepartamentoDAO.listar()
    if not deptos:
        depto_demo = DepartamentoDAO.insertar(Departamento(nombre="Tecnología"))
        print(f"Departamento creado: {depto_demo.nombre} (ID: {depto_demo.id})")
    else:
        depto_demo = deptos[0]
        print(f"Usando departamento existente: {depto_demo.nombre}")

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
            # Corrección de firma: departamento_id enviado como argumento nombrado
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

    # 3. Cargar Usuarios para Login (Admin y Empleado estándar)
    if empleados_creados:
        # Crear Admin vinculado al primer empleado
        emp_admin = empleados_creados[0]
        user_admin = UsuarioDAO.buscar_por_nombre_usuario("admin")
        if not user_admin:
            usuario_admin = Usuario(
                empleado_id=emp_admin.id,
                nombre_usuario="admin",
                password_hash="admin123",  # En producción usar hash (ej. bcrypt)
                rol="admin",
            )
            UsuarioDAO.insertar(usuario_admin)
            print(f"Usuario 'admin' creado correctamente (Password: admin123)")

        # Crear Usuario estándar vinculado al segundo empleado
        if len(empleados_creados) > 1:
            emp_user = empleados_creados[1]
            user_std = UsuarioDAO.buscar_por_nombre_usuario("cmendoza")
            if not user_std:
                usuario_std = Usuario(
                    empleado_id=emp_user.id,
                    nombre_usuario="cmendoza",
                    password_hash="user123",
                    rol="empleado",
                )
                UsuarioDAO.insertar(usuario_std)
                print(f"Usuario 'cmendoza' creado correctamente (Password: user123)")


if __name__ == "__main__":
    cargar_datos_semilla()
    print("Semilla ejecutada con éxito.")