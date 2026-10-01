from dominio.empleado import Empleado
empleado = Empleado(
nombre="Ana Torres",
correo="ana.torres@ecotech.cl")
print(empleado.mostrar_datos())

from persistencia.crear_bd import crear_tablas
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

crear_tablas()
empleado = Empleado(nombre="Ana Pérez", correo="ana@ecotech.cl")

print("Antes:", empleado.id)
# None

EmpleadoDAO.insertar(empleado)

print("Después:", empleado.id)
# id generado por la BD