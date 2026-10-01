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
    
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, marcador_sql

class EmpleadoDAO:
    @staticmethod
    def insertar(empleado):
        pass
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
