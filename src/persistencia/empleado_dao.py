from persistencia.conexion import abrir_conexion, obtener_motor

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        sql = f"""
            INSERT INTO empleado (nombre, correo)
            VALUES ({marcador}, {marcador})
        """
        cursor.execute(sql, (empleado.nombre, empleado.correo))
        empleado.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return empleado

#clase 5
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
    ….

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()

        marca = marcador_sql()
        sql = f"""
                    SELECT id, nombre, correo
                    FROM empleado WHERE id = {marca}
                """
        cursor.execute(sql, (id_empleado,))
        fila = cursor.fetchone()
        conexion.close()

        if fila is None:
            return None
return Empleado(id=fila[0], nombre=fila[1], correo=fila[2])

#revisar lo que esta bajo este comentario

    @staticmethod
    def buscar_por_correo(correo):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT {_COLUMNAS} FROM empleado WHERE correo = {marca}", (correo,)
            )
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
                f"SELECT {_COLUMNAS} FROM empleado "
                f"WHERE departamento_id = {marca} ORDER BY id",
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
                "UPDATE empleado "
                f"SET nombre = {marca}, correo = {marca}, departamento_id = {marca} "
                f"WHERE id = {marca}",
                (empleado.nombre, empleado.correo, empleado.departamento_id, empleado.id),
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
