from conexion import abrir_conexion, obtener_motor

def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    motor = obtener_motor()

    if motor == "sqlite":
        # Tabla Departamento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        ''')

        # Tabla Empleado (un departamento puede tener 0 a muchos empleados)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                direccion TEXT,
                telefono TEXT,
                departamento_id INTEGER,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE SET NULL
            )
        ''')

        # Tabla Usuario (para login/autenticación y definición del rol admin/empleado)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                rol TEXT NOT NULL DEFAULT 'empleado',
                empleado_id INTEGER UNIQUE,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE,
                CHECK (rol IN ('admin', 'empleado'))
            )
        ''')

    else:  # MySQL
        # Tabla Departamento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departamento (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL
            ) ENGINE=InnoDB;
        ''')

        # Tabla Empleado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleado (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) NOT NULL UNIQUE,
                direccion VARCHAR(255),
                telefono VARCHAR(20),
                departamento_id INT,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id) ON DELETE SET NULL
            ) ENGINE=InnoDB;
        ''')

        # Tabla Usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                rol ENUM('admin', 'empleado') NOT NULL DEFAULT 'empleado',
                empleado_id INT UNIQUE,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
        ''')

    conexion.commit()
    cursor.close()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos y tablas creadas correctamente.")