from utilidades import entero_positivo, texto_no_vacio


class Usuario:
    MIN_USUARIO = 3
    MAX_USUARIO = 40
    MIN_CLAVE = 6
    ROLES = ("admin", "empleado")

    def __init__(self, nombre_usuario, password_hash, empleado_id, rol="empleado", id=None):
        self.id = id
        self.empleado_id = empleado_id
        self.nombre_usuario = nombre_usuario
        self.password_hash = password_hash
        self.rol = rol

    # -------------------------------------------------------------------------
    # Validaciones y Reglas de Negocio
    # -------------------------------------------------------------------------
    @classmethod
    def normalizar_usuario(cls, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El usuario debe ser texto.")
        nombre = nombre.strip().lower()
        if not cls.MIN_USUARIO <= len(nombre) <= cls.MAX_USUARIO:
            raise ValueError(f"El usuario debe tener entre {cls.MIN_USUARIO} y {cls.MAX_USUARIO} caracteres.")
        if not all(c.isascii() and (c.isalnum() or c == "_") for c in nombre):
            raise ValueError("Use letras ASCII, números o guion bajo.")
        return nombre

    @classmethod
    def validar_clave(cls, clave):
        if not isinstance(clave, str):
            raise TypeError("La contraseña debe ser texto.")
        if len(clave) < cls.MIN_CLAVE:
            raise ValueError(f"Use al menos {cls.MIN_CLAVE} caracteres.")
        return clave  # Sin strip, lower ni truncado.

    @classmethod
    def validar_rol(cls, rol):
        if not isinstance(rol, str) or rol not in cls.ROLES:
            raise ValueError(f"Rol no permitido. Debe ser uno de: {', '.join(cls.ROLES)}")
        return rol

    # -------------------------------------------------------------------------
    # Encapsulamiento (Getters y Setters)
    # -------------------------------------------------------------------------
    @property
    def empleado_id(self):
        return self._empleado_id

    @empleado_id.setter
    def empleado_id(self, valor):
        self._empleado_id = entero_positivo(valor, "El ID del empleado")

    @property
    def nombre_usuario(self):
        return self._nombre_usuario

    @nombre_usuario.setter
    def nombre_usuario(self, valor):
        self._nombre_usuario = self.normalizar_usuario(valor)

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, valor):
        self._password_hash = texto_no_vacio(valor, "El hash de la contraseña")

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        self._rol = self.validar_rol(valor)

    # -------------------------------------------------------------------------
    # Métodos Auxiliares
    # -------------------------------------------------------------------------
    def mostrar_datos(self):
        return f"[{self.id}] Usuario: {self.nombre_usuario} (Rol: {self.rol}, Empleado ID: {self.empleado_id})"

    def __str__(self):
        return self.mostrar_datos()