class Empleado:
    def __init__(self,nombre,correo):
        self.nombre = nombre
        self.correo = correo
    def mostrar_datos(self) -> str:
        return f"{self.nombre} - {self.correo}"