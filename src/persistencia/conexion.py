import os
import sqlite3
import pymysql
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()


class ErrorConfiguracion(Exception):
    """Error de configuración de la base de datos."""


class ErrorBaseDatos(RuntimeError):
    """Error de conexión expuesto de forma segura a la aplicación."""


ERRORES_BD = (sqlite3.Error, pymysql.MySQLError, ErrorBaseDatos)
ERRORES_INTEGRIDAD = (sqlite3.IntegrityError, pymysql.err.IntegrityError)


def obtener_motor() -> str:
    motor = os.getenv("DB_ENGINE", "sqlite").strip().lower()
    if motor not in ("sqlite", "mysql"):
        raise ErrorConfiguracion(f"Motor no soportado: {motor}")
    return motor


def _obtener_puerto_mysql() -> int:
    try:
        puerto = int(os.getenv("DB_PORT", "3306"))
    except ValueError:
        raise ErrorConfiguracion("DB_PORT debe ser un número entero.") from None
    if not 1 <= puerto <= 65535:
        raise ErrorConfiguracion("DB_PORT debe estar entre 1 y 65535.")
    return puerto


def abrir_conexion():
    motor = obtener_motor()
    try:
        if motor == "sqlite":
            conexion = sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))
            conexion.execute("PRAGMA foreign_keys = ON")
            return conexion
        elif motor == "mysql":
            return pymysql.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=_obtener_puerto_mysql(),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                charset="utf8mb4",
            )
    except (sqlite3.Error, pymysql.MySQLError) as e:
        # The UI shows a generic message while the chained cause remains available to logs.
        raise ErrorBaseDatos("Error al conectar con la base de datos.") from e

def marcador_sql() -> str:
    return "?" if obtener_motor() == "sqlite" else "%s"

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
            # CORRECCIÓN: Garantía de cierre de conexión en el bloque 'finally'.
            # POR QUÉ: Evita fugas de memoria y bloqueos de tablas en la base de datos (connection leaks).
            conexion.close()