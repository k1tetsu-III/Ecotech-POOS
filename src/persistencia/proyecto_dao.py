from dominio.proyecto import Proyecto
from persistencia.conexion import conexion_segura, marcador_sql

_COLUMNAS = "id, nombre, descripcion, pais"


class ProyectoDAO:
    """Persistencia de Proyecto. El SQL vive aquí y en ningún otro lugar."""

    @staticmethod
    def _fila_a_proyecto(fila):
        return Proyecto(
            id=fila[0], nombre=fila[1], descripcion=fila[2], pais=fila[3]
        )

    @staticmethod
    def insertar(proyecto):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT 1 FROM proyecto WHERE nombre = {marca} LIMIT 1",
                (proyecto.nombre,),
            )
            if cursor.fetchone() is not None:
                raise ValueError("Ya existe un proyecto con ese nombre.")
            cursor.execute(
                f"INSERT INTO proyecto (nombre, descripcion, pais) "
                f"VALUES ({marca}, {marca}, {marca})",
                (proyecto.nombre, proyecto.descripcion, proyecto.pais),
            )
            proyecto.id = cursor.lastrowid
        return proyecto

    @staticmethod
    def buscar_por_id(id_proyecto):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT {_COLUMNAS} FROM proyecto WHERE id = {marca}", (id_proyecto,)
            )
            fila = cursor.fetchone()
        return None if fila is None else ProyectoDAO._fila_a_proyecto(fila)

    @staticmethod
    def listar():
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM proyecto ORDER BY id")
            filas = cursor.fetchall()
        return [ProyectoDAO._fila_a_proyecto(f) for f in filas]

    @staticmethod
    def actualizar(proyecto):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"SELECT 1 FROM proyecto WHERE id = {marca}",
                (proyecto.id,),
            )
            if cursor.fetchone() is None:
                return False

            cursor.execute(
                f"SELECT 1 FROM proyecto "
                f"WHERE nombre = {marca} AND id <> {marca} LIMIT 1",
                (proyecto.nombre, proyecto.id),
            )
            if cursor.fetchone() is not None:
                raise ValueError("Ya existe un proyecto con ese nombre.")

            cursor.execute(
                f"UPDATE proyecto SET nombre = {marca}, descripcion = {marca}, "
                f"pais = {marca} "
                f"WHERE id = {marca}",
                (proyecto.nombre, proyecto.descripcion, proyecto.pais, proyecto.id),
            )
            filas_afectadas = cursor.rowcount
            if filas_afectadas > 0:
                return True

            cursor.execute(
                f"SELECT 1 FROM proyecto WHERE id = {marca}",
                (proyecto.id,),
            )
            return cursor.fetchone() is not None

    @staticmethod
    def eliminar(id_proyecto):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"DELETE FROM proyecto WHERE id = {marca}", (id_proyecto,))
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0
