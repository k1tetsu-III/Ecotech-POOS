from utilidades import texto_no_vacio

class Departamento:

    def __init__(self, nombre, id=None):
        self.id = id
        self.nombre = nombre
        self._empleados = []

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = texto_no_vacio(valor, "El nombre del departamento")

    @property
    def empleados(self):
        return tuple(self._empleados)

    def cantidad_empleados(self):
        return len(self._empleados)

    def agregar_empleado(self, empleado):
        from .empleado import Empleado

        if not isinstance(empleado, Empleado):
            raise ValueError("Solo se pueden agregar objetos de tipo Empleado.")

        if empleado.departamento_id not in (None, self.id):
            raise ValueError("El empleado ya pertenece a otro departamento.")

        for existente in self._empleados:
            if existente is empleado or (
                empleado.id is not None and existente.id == empleado.id
            ):
                return False

        if self.id is not None and empleado.departamento_id is None:
            empleado.departamento_id = self.id

        self._empleados.append(empleado)
        return True

    def mostrar_datos(self):
        return f"[{self.id}] {self.nombre} ({self.cantidad_empleados()} empleados)"

    def __str__(self):
        return self.mostrar_datos()