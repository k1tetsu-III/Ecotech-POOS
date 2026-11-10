from persistencia.conexion import conexion_segura, obtener_motor


_TABLAS_SQLITE = (
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT NOT NULL UNIQUE,
        direccion TEXT,
        telefono TEXT,
        departamento_id INTEGER,
        FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'empleado',
        empleado_id INTEGER UNIQUE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
        CHECK (rol IN ('admin', 'empleado'))
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL DEFAULT '',
        pais TEXT NOT NULL DEFAULT 'Chile'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER NOT NULL,
        proyecto_id INTEGER NOT NULL,
        fecha DATE NOT NULL,
        horas REAL NOT NULL CHECK (horas > 0 AND horas <= 24),
        descripcion TEXT NOT NULL DEFAULT '',
        FOREIGN KEY (empleado_id) REFERENCES empleado(id),
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS historial_clima (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ciudad TEXT NOT NULL,
        temperatura REAL NOT NULL,
        condicion TEXT NOT NULL,
        humedad INTEGER NOT NULL,
        fecha_consulta DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS historial_indicador (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_moneda TEXT NOT NULL,
        valor REAL NOT NULL,
        fecha_consulta DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """,
)

_TABLAS_MYSQL = (
    """
    CREATE TABLE IF NOT EXISTS departamento (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL
    ) ENGINE=InnoDB
    """,
    """
    CREATE TABLE IF NOT EXISTS empleado (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        correo VARCHAR(150) NOT NULL UNIQUE,
        direccion VARCHAR(255),
        telefono VARCHAR(20),
        departamento_id INT,
        FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE SET NULL
    ) ENGINE=InnoDB
    """,
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        rol ENUM('admin', 'empleado') NOT NULL DEFAULT 'empleado',
        empleado_id INT UNIQUE,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
    ) ENGINE=InnoDB
    """,
    """
    CREATE TABLE IF NOT EXISTS proyecto (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        descripcion VARCHAR(255) NOT NULL DEFAULT '',
        pais VARCHAR(100) NOT NULL DEFAULT 'Chile'
    ) ENGINE=InnoDB
    """,
    """
    CREATE TABLE IF NOT EXISTS registro_tiempo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        empleado_id INT NOT NULL,
        proyecto_id INT NOT NULL,
        fecha DATE NOT NULL,
        horas DECIMAL(5, 2) NOT NULL,
        descripcion VARCHAR(255) NOT NULL DEFAULT '',
        FOREIGN KEY (empleado_id) REFERENCES empleado(id),
        FOREIGN KEY (proyecto_id) REFERENCES proyecto(id),
        CHECK (horas > 0 AND horas <= 24)
    ) ENGINE=InnoDB
    """,
    """
    CREATE TABLE IF NOT EXISTS historial_clima (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ciudad VARCHAR(100) NOT NULL,
        temperatura FLOAT NOT NULL,
        condicion VARCHAR(100) NOT NULL,
        humedad INT NOT NULL,
        fecha_consulta DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """,
    """
    CREATE TABLE IF NOT EXISTS historial_indicador (
        id INT AUTO_INCREMENT PRIMARY KEY,
        codigo_moneda VARCHAR(10) NOT NULL,
        valor FLOAT NOT NULL,
        fecha_consulta DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB
    """,
)


def crear_tablas():
    motor = obtener_motor()
    sentencias = _TABLAS_SQLITE if motor == "sqlite" else _TABLAS_MYSQL
    with conexion_segura() as conexion:
        cursor = conexion.cursor()
        try:
            for sentencia in sentencias:
                cursor.execute(sentencia)
            if motor == "sqlite":
                cursor.execute("PRAGMA table_info(proyecto)")
                columnas_proyecto = {fila[1] for fila in cursor.fetchall()}
                if "pais" not in columnas_proyecto:
                    cursor.execute(
                        "ALTER TABLE proyecto ADD COLUMN "
                        "pais TEXT NOT NULL DEFAULT 'Chile'"
                    )

                cursor.execute(
                    "CREATE UNIQUE INDEX IF NOT EXISTS "
                    "uq_departamento_nombre ON departamento (nombre)"
                )
                cursor.execute(
                    "CREATE UNIQUE INDEX IF NOT EXISTS "
                    "uq_proyecto_nombre ON proyecto (nombre)"
                )
            else:
                cursor.execute("SHOW COLUMNS FROM proyecto LIKE %s", ("pais",))
                if cursor.fetchone() is None:
                    cursor.execute(
                        "ALTER TABLE proyecto ADD COLUMN "
                        "pais VARCHAR(100) NOT NULL DEFAULT 'Chile'"
                    )

                cursor.execute(
                    "SHOW INDEX FROM departamento WHERE Key_name = %s",
                    ("uq_departamento_nombre",),
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "CREATE UNIQUE INDEX uq_departamento_nombre "
                        "ON departamento (nombre)"
                    )
                cursor.execute(
                    "SHOW INDEX FROM proyecto WHERE Key_name = %s",
                    ("uq_proyecto_nombre",),
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "CREATE UNIQUE INDEX uq_proyecto_nombre "
                        "ON proyecto (nombre)"
                    )
        finally:
            cursor.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos y tablas actualizadas correctamente.")
