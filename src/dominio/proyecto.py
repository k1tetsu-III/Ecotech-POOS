from utilidades import texto_no_vacio, texto_opcional


class Proyecto:
    """Iniciativa de EcoTech en la que los empleados registran horas."""

    def __init__(self, nombre, descripcion="", id=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = texto_no_vacio(valor, "El nombre del proyecto")

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = texto_opcional(valor, "La descripción")

    def mostrar_datos(self):
        detalle = f" - {self.descripcion}" if self.descripcion else ""
        return f"[{self.id}] {self.nombre}{detalle}"

    def __str__(self):
        return self.mostrar_datos()
