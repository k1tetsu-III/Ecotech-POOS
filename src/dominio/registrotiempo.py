from utilidades import (
    entero_positivo,
    fecha_valida,
    horas_validas,
    texto_opcional,
)


class RegistroTiempo:
    """Horas dedicadas por un Empleado a un Proyecto en una fecha.

    UML: Empleado 1 ---- 0..* RegistroTiempo 0..* ---- 1 Proyecto.
    Es la clase que conserva la información propia de la relación.
    """

    def __init__(self, empleado_id, proyecto_id, fecha, horas, descripcion="", id=None):
        self.id = id
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion

    @property
    def empleado_id(self):
        return self._empleado_id

    @empleado_id.setter
    def empleado_id(self, valor):
        self._empleado_id = entero_positivo(valor, "El empleado")

    @property
    def proyecto_id(self):
        return self._proyecto_id

    @proyecto_id.setter
    def proyecto_id(self, valor):
        self._proyecto_id = entero_positivo(valor, "El proyecto")

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = fecha_valida(valor)

    @property
    def horas(self):
        return self._horas

    @horas.setter
    def horas(self, valor):
        self._horas = horas_validas(valor)

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = texto_opcional(valor, "La descripción")

    def mostrar_datos(self):
        return (
            f"[{self.id}] {self.fecha} - empleado {self.empleado_id} - "
            f"proyecto {self.proyecto_id} - {self.horas} h"
            + (f" - {self.descripcion}" if self.descripcion else "")
        )

    def __str__(self):
        return self.mostrar_datos()
