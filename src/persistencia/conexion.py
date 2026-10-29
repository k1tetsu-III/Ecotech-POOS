import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()

def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()

def abrir_conexion():
    motor = obtener_motor()

    if motor == "sqlite":
        return sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))

    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
        )
    raise ValueError(f"Motor no soportado: {motor}")

#clase 5
def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"

#revisar abajo de este comentario
@contextmanager
def conexion_segura():
    """Abre una conexión y garantiza commit, rollback y cierre.

    Uso en un DAO:
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            ...
    - Si el bloque termina bien: commit.
    - Si ocurre una excepción: rollback y la excepción se propaga
      (el DAO detecta el fallo; la aplicación decide qué mostrar).
    - Siempre: se cierra la conexión.
    """
    conexion = None
    try:
        conexion = abrir_conexion()
        yield conexion
        conexion.commit()
    except Exception:
        if conexion is not None:
            conexion.rollback()
        raise
    finally:
        if conexion is not None:
            conexion.close()
