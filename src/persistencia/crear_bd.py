"""Crea las tablas del sistema (idempotente: se puede ejecutar varias veces)."""
from persistencia.conexion import conexion_segura, obtener_motor

# Orden importante: primero las tablas referenciadas por claves foráneas.
TABLAS_SQLITE = [
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        departamento_id INTEGER,
        FOREIGN KEY (departamento_id) REFERENCES departamento(id)
            ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        descripcion TEXT NOT NULL DEFAULT ''
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER NOT NULL,
        proyecto_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        horas REAL NOT NULL CHECK (horas > 0 AND horas <= 24),
        descripcion TEXT NOT NULL DEFAULT '',
        FOREIGN KEY (empleado_id) REFERENCES empleado(id),
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
    )
    """,
]

TABLAS_MYSQL = [
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        correo VARCHAR(150) NOT NULL UNIQUE,
        departamento_id INT NULL,
        FOREIGN KEY (departamento_id) REFERENCES departamento(id)
            ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        descripcion VARCHAR(255) NOT NULL DEFAULT ''
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INT PRIMARY KEY AUTO_INCREMENT,
        empleado_id INT NOT NULL,
        proyecto_id INT NOT NULL,
        fecha DATE NOT NULL,
        horas DECIMAL(5,2) NOT NULL CHECK (horas > 0 AND horas <= 24),
        descripcion VARCHAR(255) NOT NULL DEFAULT '',
        FOREIGN KEY (empleado_id) REFERENCES empleado(id),
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
    )
    """,
]


def crear_tablas():
    sentencias = TABLAS_SQLITE if obtener_motor() == "sqlite" else TABLAS_MYSQL
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        for sql in sentencias:
            cursor.execute(sql)


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")
