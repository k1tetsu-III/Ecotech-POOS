from utilidades import texto_no_vacio, texto_opcional

class Proyecto:
    """Iniciativa de EcoTech en la que los empleados registran horas."""

    # CORRECCIÓN: Se incorpora el atributo 'pais' (por defecto 'Chile').
    # POR QUÉ: Permite vincular la entidad Proyecto con los servicios de API externa (clima por ubicación y tipo de cambio internacional)[cite: 42].
    def __init__(self, nombre, descripcion="", pais="Chile", id=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.pais = pais

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

    # CORRECCIÓN: Getter y Setter para el nuevo campo 'pais'.
    # POR QUÉ: Aplica encapsulation y valida que el campo no contenga cadenas vacías o no válidas.
    @property
    def pais(self):
        return self._pais

    @pais.setter
    def pais(self, valor):
        self._pais = texto_no_vacio(valor, "El país del proyecto")

    def mostrar_datos(self):
        detalle = f" - {self.descripcion}" if self.descripcion else ""
        return f"[{self.id}] {self.nombre} ({self.pais}){detalle}"

    def __str__(self):
        return self.mostrar_datos()