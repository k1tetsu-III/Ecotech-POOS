## Integrante
| Integrante |
|---|---|---|
| _Octavio Pizarro_ |

## Requisitos

- Python 3.10 o superior
- Git
- (Opcional) un servidor MySQL, solo si usarán `DB_ENGINE=mysql`

## Cómo ejecutarlo (paso a paso, en un equipo limpio)

Comandos para **Git Bash en Windows** 

```bash
# 1. Clonar el repositorio y entrar a la carpeta
git clone https://github.com/<usuario>/Ecotech_Poos.git
cd Ecotech_Poos

# 2. Crear y activar el entorno virtual
py -m venv .venv
source .venv/Scripts/activate

# 3. Instalar las dependencias
python -m pip install -r requirements.txt

# 4. Crear la configuración local (queda fuera de Git)
cp .env.example .env

```

Con el `.env` por defecto se usa **SQLite**: el archivo `ecotech.db` y las
tablas se crean solos al iniciar. No hay que instalar ni configurar nada más.

<details>
<summary>PowerShell</summary>

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1     
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python src/main.py
```
</details>

### Usar MySQL en vez de SQLite

1. Crear la base y un usuario en MySQL (ejemplo):
   ```sql
   CREATE DATABASE ecotech CHARACTER SET utf8mb4;
   CREATE USER 'ecotech_app'@'localhost' IDENTIFIED BY 'cambia_esta_clave';
   GRANT ALL PRIVILEGES ON ecotech.* TO 'ecotech_app'@'localhost';
   ```
2. Editar `.env`:
   ```
   DB_ENGINE=mysql
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=ecotech
   DB_USER=ecotech_app
   DB_PASSWORD=cambia_esta_clave
   ```
3. Ejecutar `python src/main.py`. Las tablas se crean al iniciar.

No hay que cambiar código: solo `DB_ENGINE` y los datos de conexión en `.env`.
El archivo `.env` contiene credenciales y **nunca se sube a Git**
(`.env.example` documenta las variables sin secretos).

## Estructura del proyecto

```
Ecotech_Poos/
├── src/
│   ├── main.py                    # punto de entrada y menú principal
│   ├── menu_empleado.py           # interacción de cada área
│   ├── menu_departamento.py
│   ├── menu_proyecto.py
│   ├── menu_registrotiempo.py
│   ├── menu_comun.py              # entrada por consola y manejo de errores de menú
│   ├── utilidades.py              # validadores reutilizables
│   ├── dominio/                   # clases del problema (no conocen SQL)
│   │   ├── empleado.py
│   │   ├── departamento.py
│   │   ├── proyecto.py
│   │   └── registrotiempo.py
│   └── persistencia/              # acceso a datos
│       ├── conexion.py            # SQLite/MySQL, commit/rollback/cierre
│       ├── crear_bd.py            # creación de tablas
│       ├── empleado_dao.py
│       ├── departamento_dao.py
│       ├── proyecto_dao.py
│       └── registrotiempo_dao.py
├── docs/modelo.md                 # UML, relaciones y tablas
├── .env.example · .gitignore · requirements.txt · README.md
```

El modelo (UML → clases → tablas) está en [`docs/modelo.md`](docs/modelo.md).

## Qué hace la aplicación

CRUD completo (registrar, listar/buscar, actualizar, eliminar) para las cuatro
entidades. Reglas relevantes:

- Un empleado pertenece como máximo a un departamento; al eliminar un
  departamento sus empleados quedan sin departamento.
- Un registro de tiempo exige empleado y proyecto existentes, fecha válida y
  horas entre 0 y 24.
- No se puede eliminar un empleado o proyecto que tenga registros de tiempo.
- El correo del empleado y los nombres de departamento/proyecto son únicos.

## Decisiones de diseño (para la defensa)

- **UML → Python:** cada clase del UML es una clase en `dominio/`; las
  multiplicidades 0..* se representan con una colección (`Departamento._empleados`)
  y las claves foráneas en la BD (`departamento_id`, `empleado_id`, `proyecto_id`).
- **Encapsulamiento:** atributos con `_` y `@property` con validación; la lista
  interna de empleados solo se expone como tupla de solo lectura.
- **Sin duplicación:** los validadores están en `utilidades.py` y los usan el
  dominio y los menús; `conexion_segura()` centraliza commit/rollback/cierre
  para todos los DAO.
- **Herencia:** no se usa porque el modelo no tiene especializaciones reales de
  comportamiento (la jefatura sería un rol/asociación, no un subtipo).
- **Seguridad en base de datos:** todas las consultas son parametrizadas
  (`?` en SQLite, `%s` en MySQL, resuelto en `marcador_sql()`); las credenciales
  van en `.env`; en SQLite se activan las claves foráneas por conexión.
- **Excepciones:**
  - `conexion_segura()` hace `try/except/finally`: commit si todo sale bien,
    rollback si falla y cierre de la conexión siempre.
  - `operacion_segura` (en `menu_comun.py`) separa tres casos: `ValueError`
    (dato inválido), `ERRORES_INTEGRIDAD` (duplicado o relación) y `ERRORES_BD`
    (conexión, SQL, etc.). El usuario ve un mensaje seguro; el detalle técnico
    se guarda en `ecotech.log`.
  - Resultados normales no son excepciones: buscar un ID inexistente devuelve
    `None` y eliminar/actualizar devuelven `False`.
- **Validación vs. excepción:** `pedir()` valida la entrada y vuelve a preguntar;
  las excepciones quedan para fallos reales.

## Pruebas manuales sugeridas

1. Registrar un departamento, un empleado en ese departamento y un proyecto.
2. Registrar horas para ese empleado y proyecto; listar por empleado y proyecto.
3. Probar entradas inválidas: correo sin `@`, ID con letras, fecha `2026-13-45`,
   horas `30`, opción de menú fuera de rango.
4. Registrar un correo repetido → mensaje de duplicado, sin cerrar el programa.
5. Eliminar un empleado con horas registradas → se rechaza con mensaje seguro.
6. Poner un `DB_NAME` inválido en `.env` → mensaje de conexión, sin traceback.

## Flujo de trabajo en equipo

- Cada integrante trabaja en su rama (`feature/...`) y hace commits propios.
- Antes de integrar: `git pull`, ejecutar la aplicación y revisar los cambios.
- Se integra a `main` mediante Pull Request.

## Registro de uso de herramientas de IA

se le solicito a la ia actuar de ayudante, sin modificar, solamente sugerir, cuando se acordo realizar el cambio, se solicito realizarlo. 
## IMPORTANTE ---Aun faltan cosas por documentar, falta completar algunas funciones y arreglar algunas carpetas--- plazo hasta el lunes(posiblemente)
