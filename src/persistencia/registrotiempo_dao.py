from dominio.registrotiempo import RegistroTiempo
from persistencia.conexion import conexion_segura, marcador_sql

_COLUMNAS = "id, empleado_id, proyecto_id, fecha, horas, descripcion"


class RegistroTiempoDAO:
    """Persistencia de RegistroTiempo (la relación Empleado–Proyecto)."""

    @staticmethod
    def _fila_a_registro(fila):
        return RegistroTiempo(
            id=fila[0], empleado_id=fila[1], proyecto_id=fila[2],
            fecha=fila[3], horas=fila[4], descripcion=fila[5],
        )

    @staticmethod
    def insertar(registro):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO registro_tiempo "
                "(empleado_id, proyecto_id, fecha, horas, descripcion) "
                f"VALUES ({marca}, {marca}, {marca}, {marca}, {marca})",
                (registro.empleado_id, registro.proyecto_id,
                 registro.fecha.isoformat(), registro.horas, registro.descripcion),
            )
            registro.id = cursor.lastrowid
        return registro

    @staticmethod
    def buscar_por_id(id_registro):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT {_COLUMNAS} FROM registro_tiempo WHERE id = {marca}",
                (id_registro,),
            )
            fila = cursor.fetchone()
        return None if fila is None else RegistroTiempoDAO._fila_a_registro(fila)

    @staticmethod
    def listar():
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM registro_tiempo ORDER BY fecha, id")
            filas = cursor.fetchall()
        return [RegistroTiempoDAO._fila_a_registro(f) for f in filas]

    @staticmethod
    def listar_por_empleado(id_empleado):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT {_COLUMNAS} FROM registro_tiempo "
                f"WHERE empleado_id = {marca} ORDER BY fecha, id",
                (id_empleado,),
            )
            filas = cursor.fetchall()
        return [RegistroTiempoDAO._fila_a_registro(f) for f in filas]

    @staticmethod
    def listar_por_proyecto(id_proyecto):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT {_COLUMNAS} FROM registro_tiempo "
                f"WHERE proyecto_id = {marca} ORDER BY fecha, id",
                (id_proyecto,),
            )
            filas = cursor.fetchall()
        return [RegistroTiempoDAO._fila_a_registro(f) for f in filas]

    @staticmethod
    def actualizar(registro):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE registro_tiempo "
                f"SET empleado_id = {marca}, proyecto_id = {marca}, fecha = {marca}, "
                f"horas = {marca}, descripcion = {marca} WHERE id = {marca}",
                (registro.empleado_id, registro.proyecto_id,
                 registro.fecha.isoformat(), registro.horas,
                 registro.descripcion, registro.id),
            )
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0

    @staticmethod
    def eliminar(id_registro):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"DELETE FROM registro_tiempo WHERE id = {marca}", (id_registro,)
            )
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0
