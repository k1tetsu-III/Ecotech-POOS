# Ecotech POOS

## Descripción

Aplicación de consola para gestionar empleados, departamentos, proyectos,
registros de tiempo y cuentas de usuario. Permite operaciones CRUD para las
cuatro entidades principales y utiliza SQLite por defecto o MySQL de forma
opcional.

## Integrante

| Integrante |
|---|
| _Octavio Pizarro_ |

## Requisitos

- Python 3.10 o superior
- Git
- (Opcional) un servidor MySQL, solo si se usa `DB_ENGINE=mysql`

## Instalación y ejecución

### Git Bash en Windows

```bash
# 1. Clonar el repositorio y entrar a la carpeta
git clone https://github.com/k1tetsu-III/Ecotech-POOS.git
cd Ecotech-POOS

# 2. Crear y activar el entorno virtual
py -m venv .venv
source .venv/Scripts/activate

# 3. Instalar las dependencias
python -m pip install -r requirements.txt

# 4. Crear la configuración local y definir las contraseñas de demostración
cp .env.example .env
# Edita .env y define ECOTECH_SEED_ADMIN_PASSWORD y
# ECOTECH_SEED_EMPLOYEE_PASSWORD con contraseñas propias.

# 5. Crear las tablas y cuentas de demostración
python src/semilla_bd.py

# 6. Iniciar sesión en la aplicación
python src/main.py
```

### PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edita .env y define las contraseñas de demostración antes de continuar.
python src/semilla_bd.py
python src/main.py
```

Con la configuración predeterminada se usa **SQLite**: el archivo `ecotech.db`
y las tablas se crean al iniciar la aplicación.

## Configuración de la base de datos

El archivo `.env` contiene la configuración local y puede incluir credenciales;
**no debe subirse a Git**. `.env.example` sirve como plantilla sin secretos.

### Usar MySQL en vez de SQLite

1. Crear la base y un usuario en MySQL (ejemplo):

   ```sql
   CREATE DATABASE ecotech CHARACTER SET utf8mb4;
   CREATE USER 'ecotech_app'@'localhost' IDENTIFIED BY 'cambia_esta_clave';
   GRANT ALL PRIVILEGES ON ecotech.* TO 'ecotech_app'@'localhost';
   ```

2. Configurar `.env`:

   ```text
   DB_ENGINE=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ecotech
   DB_USER=ecotech_app
   DB_PASSWORD=cambia_esta_clave
   ```

3. Ejecutar `python src/main.py`. Las tablas se crean al iniciar.

No es necesario cambiar el código para alternar motores; basta con configurar
`DB_ENGINE` y los datos de conexión en `.env`.

## Datos de demostración

Para crear las cuentas iniciales, configura `ECOTECH_SEED_ADMIN_PASSWORD` y
`ECOTECH_SEED_EMPLOYEE_PASSWORD` en el `.env` local con contraseñas propias
(mínimo 6 y máximo 72 bytes UTF-8), y ejecuta:

```powershell
python src/semilla_bd.py
```

La semilla no imprime las contraseñas ni modifica cuentas ya existentes.

## Funcionalidades y reglas

- Gestión CRUD de empleados, departamentos, proyectos y registros de tiempo.
- Las cuentas de usuario solo las puede crear un administrador para un empleado
  existente que aún no tenga una cuenta; los empleados no pueden asociar una
  cuenta a otro ID.
- Un empleado pertenece como máximo a un departamento; al eliminar un
  departamento, sus empleados quedan sin departamento.
- Un registro de tiempo requiere un empleado y un proyecto existentes, una
  fecha válida y horas entre 0.01 y 24 (redondeadas a dos decimales).
- No se puede eliminar un empleado o proyecto que tenga registros de tiempo.
- El correo del empleado y los nombres de departamento y proyecto son únicos.

## Estructura del proyecto

```text
Ecotech-POOS/
├── src/
│   ├── main.py                    # punto de entrada y menú principal
│   ├── menu_empleado.py           # menús de las áreas
│   ├── menu_departamento.py
│   ├── menu_proyecto.py
│   ├── menu_registrotiempo.py
│   ├── menu_usuario.py
│   ├── menu_comun.py              # entrada por consola y manejo de errores
│   ├── utilidades.py              # validadores reutilizables
│   ├── semilla_bd.py              # carga de datos de demostración
│   ├── dominio/                   # clases del problema, sin SQL
│   ├── persistencia/              # conexión, esquema y DAO
│   └── servicios/                 # autenticación y lógica de servicios
├── docs/modelo.md                 # UML, relaciones y tablas
├── .env.example
├── .gitignore
└── requirements.txt
```

El modelo (UML → clases → tablas) está en [`docs/modelo.md`](docs/modelo.md).

## Decisiones de diseño

- **UML → Python:** cada clase del UML está en `dominio/`; las multiplicidades
  0..* se representan con una colección (`Departamento._empleados`) y las
  claves foráneas en la base de datos (`departamento_id`, `empleado_id`,
  `proyecto_id`).
- **Encapsulamiento:** atributos con `_` y propiedades (`@property`) con
  validación; la lista interna de empleados solo se expone como tupla de solo
  lectura.
- **Sin duplicación:** los validadores están en `utilidades.py` y los usan el
  dominio y los menús; `conexion_segura()` centraliza commit, rollback y cierre
  para los DAO.
- **Herencia:** no se usa porque el modelo no tiene especializaciones reales de
  comportamiento (la jefatura sería un rol o asociación, no un subtipo).
- **Seguridad en base de datos:** las consultas son parametrizadas (`?` en
  SQLite, `%s` en MySQL, resuelto en `marcador_sql()`); las credenciales se
  guardan en `.env`; SQLite activa las claves foráneas por conexión.
- **Excepciones:**
  - `conexion_segura()` confirma si todo sale bien, revierte si falla y cierra
    siempre la conexión.
  - `operacion_segura` (en `menu_comun.py`) distingue datos inválidos,
    violaciones de integridad y errores de base de datos. El usuario ve un
    mensaje seguro y el detalle técnico se guarda en `ecotech.log`.
  - Buscar un ID inexistente devuelve `None`; eliminar y actualizar devuelven
    `False` si no encuentran el registro.
- **Validación vs. excepción:** `pedir()` valida la entrada y vuelve a
  preguntar; las excepciones se reservan para fallos reales.

## Pruebas manuales sugeridas

1. Registrar un departamento, un empleado en ese departamento y un proyecto.
2. Registrar horas para ese empleado y proyecto; listar por empleado y por
   proyecto.
3. Probar entradas inválidas: correo sin `@`, ID con letras, fecha
   `2026-13-45`, horas `30` y opción de menú fuera de rango.
4. Registrar un correo repetido y comprobar que se muestra el error sin cerrar
   el programa.
5. Intentar eliminar un empleado con horas registradas y comprobar que se
   rechaza con un mensaje seguro.
6. Configurar un `DB_NAME` inválido en `.env` y comprobar que se muestra un
   mensaje de conexión sin traceback.

## Flujo de trabajo en equipo

- Cada integrante trabaja en su rama (`feature/...`) y hace sus propios
  commits.
- Antes de integrar: ejecutar `git pull`, probar la aplicación y revisar los
  cambios.
- Integrar a `main` mediante un Pull Request.

## Registro de uso de herramientas de IA

Se solicitó a la IA actuar como ayudante: primero revisar y sugerir; una vez
acordados los cambios estos se implementarlos.

### Correcciones realizadas durante la asistencia

- Se corrigieron llamadas a APIs inexistentes o incompatibles entre servicios y
  DAO, así como importaciones y flujos de menús.
- Se ajustaron validaciones de empleados, departamentos, proyectos, registros
  de tiempo e IDs; se mejoraron los mensajes y el manejo de errores de
  autenticación, base de datos y servicios externos.
- Se corrigió el flujo de sesión por rol y se restringió la creación de cuentas
  a administradores, verificando el empleado y evitando asociar cuentas a IDs
  ajenos.
- Se eliminaron credenciales fijas de la semilla: ahora las contraseñas de
  demostración se configuran localmente y no se imprimen.
- Se ampliaron las reglas de `.gitignore` y se retiraron del índice de Git el
  entorno virtual y la base local, conservándolos en el equipo.
- Se organizaron las opciones de edición para mantener o borrar campos
  opcionales.

### Sugerencias y verificaciones pendientes

- Ejecutar la aplicación y las pruebas manuales de este README en un entorno
  con Python y dependencias disponibles; la validación automatizada no pudo
  completarse durante la asistencia.
- Completar la documentación y revisar las funciones y carpetas que aún estén
  pendientes en el proyecto.
- Antes de integrar cambios, revisar el diff completo y confirmar que no se
  agreguen archivos locales, credenciales ni datos de la base.
