from utilidades import correo_valido, entero_positivo, texto_no_vacio


class Empleado:

    def __init__(self, nombre, correo, direccion=None, telefono=None, departamento_id=None, id=None):
        self.id = id  # None hasta que la base de datos lo genera
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.departamento_id = departamento_id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = texto_no_vacio(valor, "El nombre")

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = correo_valido(valor)

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = valor

    @property
    def departamento_id(self):
        return self._departamento_id

    @departamento_id.setter
    def departamento_id(self, valor):
        self._departamento_id = (
            None if valor is None else entero_positivo(valor, "El departamento")
        )

    def mostrar_datos(self):
        depto = self.departamento_id if self.departamento_id is not None else "sin departamento"
        dir_txt = self.direccion if self.direccion else "sin dirección"
        tel_txt = self.telefono if self.telefono else "sin teléfono"
        return f"[{self.id}] {self.nombre} - {self.correo} | Tel: {tel_txt} | Dir: {dir_txt} (departamento: {depto})"

    def __str__(self):
        return self.mostrar_datos() 