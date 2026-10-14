from dominio.empleado import Empleado
from utilidades import texto_no_vacio


class Departamento:
    """Unidad de EcoTech. UML: Departamento 1 ---- 0..* Empleado."""

    def __init__(self, nombre, id=None):
        self.id = id
        self.nombre = nombre
        self._empleados = []  # multiplicidad 0..* -> colección de objetos

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = texto_no_vacio(valor, "El nombre del departamento")

    @property
    def empleados(self):
        """Vista de solo lectura: no expone la lista interna."""
        return tuple(self._empleados)

    def cantidad_empleados(self):
        return len(self._empleados)

    def agregar_empleado(self, empleado):
        """Agrega un empleado. Devuelve False si ya estaba en el departamento.

        Regla UML: un empleado pertenece como máximo a un departamento.
        """
        if not isinstance(empleado, Empleado):
            raise ValueError("Solo se pueden agregar objetos Empleado.")
        if empleado.departamento_id not in (None, self.id):
            raise ValueError("El empleado ya pertenece a otro departamento.")
        for existente in self._empleados:
            if existente is empleado or (
                empleado.id is not None and existente.id == empleado.id
            ):
                return False
        self._empleados.append(empleado)
        return True

    def mostrar_datos(self):
        return f"[{self.id}] {self.nombre} ({self.cantidad_empleados()} empleados)"

    def __str__(self):
        return self.mostrar_datos()
