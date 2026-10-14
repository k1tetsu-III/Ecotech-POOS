from dominio.departamento import Departamento
from persistencia.conexion import conexion_segura, marcador_sql


class DepartamentoDAO:
    """Persistencia de Departamento. El SQL vive aquí y en ningún otro lugar."""

    @staticmethod
    def _fila_a_departamento(fila):
        return Departamento(id=fila[0], nombre=fila[1])

    @staticmethod
    def insertar(departamento):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"INSERT INTO departamento (nombre) VALUES ({marca})",
                (departamento.nombre,),
            )
            departamento.id = cursor.lastrowid
        return departamento

    @staticmethod
    def buscar_por_id(id_departamento):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT id, nombre FROM departamento WHERE id = {marca}",
                (id_departamento,),
            )
            fila = cursor.fetchone()
        return None if fila is None else DepartamentoDAO._fila_a_departamento(fila)

    @staticmethod
    def listar():
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre FROM departamento ORDER BY id")
            filas = cursor.fetchall()
        return [DepartamentoDAO._fila_a_departamento(f) for f in filas]

    @staticmethod
    def actualizar(departamento):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"UPDATE departamento SET nombre = {marca} WHERE id = {marca}",
                (departamento.nombre, departamento.id),
            )
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0

    @staticmethod
    def eliminar(id_departamento):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"DELETE FROM departamento WHERE id = {marca}", (id_departamento,)
            )
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0
