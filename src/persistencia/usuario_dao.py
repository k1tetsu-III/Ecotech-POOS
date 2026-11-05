from dominio.usuario import Usuario
from persistencia.conexion import conexion_segura, marcador_sql

_COLUMNAS = "id, empleado_id, nombre_usuario, password, rol"

class UsuarioDAO:

    @staticmethod
    def _fila_a_usuario(fila):
        return Usuario(
            id=fila[0],
            empleado_id=fila[1],
            nombre_usuario=fila[2],
            password_hash=fila[3],
            rol=fila[4]
        )

    @staticmethod
    def insertar(usuario):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            sql = f"""
                INSERT INTO usuario (empleado_id, nombre_usuario, password, rol)
                VALUES ({marca}, {marca}, {marca}, {marca})
            """
            cursor.execute(sql, (
                usuario.empleado_id,
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.rol
            ))
            usuario.id = cursor.lastrowid
        return usuario

    @staticmethod
    def buscar_por_nombre_usuario(nombre_usuario):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM usuario WHERE nombre_usuario = {marca}", (nombre_usuario,))
            fila = cursor.fetchone()
        return None if fila is None else UsuarioDAO._fila_a_usuario(fila)

    @staticmethod
    def buscar_por_empleado_id(empleado_id):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM usuario WHERE empleado_id = {marca}", (empleado_id,))
            fila = cursor.fetchone()
        return None if fila is None else UsuarioDAO._fila_a_usuario(fila)

    @staticmethod
    def listar():
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT {_COLUMNAS} FROM usuario ORDER BY id")
            filas = cursor.fetchall()
        return [UsuarioDAO._fila_a_usuario(f) for f in filas]

    @staticmethod
    def actualizar(usuario):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"""UPDATE usuario 
                    SET nombre_usuario = {marca}, password = {marca}, rol = {marca} 
                    WHERE id = {marca}""",
                (usuario.nombre_usuario, usuario.password_hash, usuario.rol, usuario.id),
            )
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0

    @staticmethod
    def eliminar(id_usuario):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(f"DELETE FROM usuario WHERE id = {marca}", (id_usuario,))
            filas_afectadas = cursor.rowcount
        return filas_afectadas > 0