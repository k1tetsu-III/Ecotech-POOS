from dominio.empleado import Empleado
from persistencia.conexion import conexion_segura, marcador_sql

_COLUMNAS = "id, nombre, correo, direccion, telefono, departamento_id"

class EmpleadoDAO:

    @staticmethod
    def _fila_a_empleado(fila):
        return Empleado(
            id=fila[0],
            nombre=fila[1],
            correo=fila[2],
            direccion=fila[3],
            telefono=fila[4],
            departamento_id=fila[5]
        )

    @staticmethod
    def insertar(empleado):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            sql = f"""
                INSERT INTO empleado (nombre, correo, direccion, telefono, departamento_id)
                VALUES ({marca}, {marca}, {marca}, {marca}, {marca})
            """
            cursor.execute(sql, (
                empleado.nombre,
                empleado.correo,
                empleado.direccion,
                empleado.telefono,
                empleado.departamento_id
            ))
            empleado.id = cursor.lastrowid
        return empleado

    @staticmethod
    def buscar_por_id(id_empleado):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM empleado WHERE id = {marca}", (id_empleado,))
            fila = cursor.fetchone()
        return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)

    @staticmethod
    def buscar_por_correo(correo):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM empleado WHERE correo = {marca}", (correo,))
            fila = cursor.fetchone()
        return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)

    @staticmethod
    def listar():
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM empleado ORDER BY id")
            filas = cursor.fetchall()
        return [EmpleadoDAO._fila_a_empleado(f) for f in filas]

    @staticmethod
    def listar_por_departamento(id_departamento):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT {_COLUMNAS} FROM empleado WHERE departamento_id = {marca} ORDER BY id",
                (id_departamento,),
            )
            filas = cursor.fetchall()
        return [EmpleadoDAO._fila_a_empleado(f) for f in filas]

    @staticmethod
    def actualizar(empleado):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"""UPDATE empleado 
                    SET nombre = {marca}, correo = {marca}, direccion = {marca}, 
                        telefono = {marca}, departamento_id = {marca} 
                    WHERE id = {marca}""",
                (
                    empleado.nombre,
                    empleado.correo,
                    empleado.direccion,
                    empleado.telefono,
                    empleado.departamento_id,
                    empleado.id
                ),
            )
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0

    @staticmethod
    def eliminar(id_empleado):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"DELETE FROM empleado WHERE id = {marca}", (id_empleado,))
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0