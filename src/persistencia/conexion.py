import os
import sqlite3
from contextlib import contextmanager

import pymysql
from dotenv import load_dotenv

load_dotenv()

# Grupos de excepciones para capturar fallos específicos de cada tipo.
ERRORES_INTEGRIDAD = (sqlite3.IntegrityError, pymysql.err.IntegrityError)
ERRORES_BD = (sqlite3.Error, pymysql.MySQLError)

def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()


def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        conexion = sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))
        # SQLite no valida claves foráneas salvo que se active en cada conexión.
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion
    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
        )
    raise ErrorConfiguracion(f"Motor no soportado: {motor}")


def marcador_sql():
    return "?" if obtener_motor() == "sqlite" else "%s"


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
