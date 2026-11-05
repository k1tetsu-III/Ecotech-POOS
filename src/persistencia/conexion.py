import os
import sqlite3
import pymysql
from contextlib import contextmanager  # <-- AGREGADO: Necesario para usar @contextmanager
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

def marcador_sql():
    if obtener_motor() == "sqlite":
        return "?"
    return "%s"

@contextmanager
def conexion_segura():
    """Abre una conexión y garantiza commit, rollback y cierre."""
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