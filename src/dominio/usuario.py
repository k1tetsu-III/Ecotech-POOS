import hashlib
import hmac
import re

import bcrypt

from utilidades import entero_positivo, texto_no_vacio


class Usuario:
    MIN_USUARIO = 3
    MAX_USUARIO = 40
    MIN_CLAVE = 6
    MAX_BYTES_BCRYPT = 72
    ROLES = ("admin", "empleado")
    _PATRON_HASH_BCRYPT = re.compile(
        r"^\$2[aby]\$(0[4-9]|[12][0-9]|3[01])\$[./A-Za-z0-9]{53}$"
    )
    _PATRON_HASH_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")

    def __init__(self, nombre_usuario, password_hash, empleado_id, rol="empleado", id=None):
        self.id = id
        self.empleado_id = empleado_id
        self.nombre_usuario = nombre_usuario
        self.password_hash = password_hash
        self.rol = rol

    @classmethod
    def encriptar_clave(cls, clave: str) -> str:
        """Genera un hash bcrypt compatible con el flujo de autenticación."""
        clave = cls.validar_clave(clave)
        clave_bytes = clave.encode("utf-8")
        if len(clave_bytes) > cls.MAX_BYTES_BCRYPT:
            raise ValueError(
                f"La contraseña no puede superar los {cls.MAX_BYTES_BCRYPT} bytes UTF-8."
            )
        return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")

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
        if len(clave.encode("utf-8")) > cls.MAX_BYTES_BCRYPT:
            raise ValueError(
                f"La contraseña no puede superar los {cls.MAX_BYTES_BCRYPT} bytes UTF-8."
            )
        return clave

    @classmethod
    def validar_rol(cls, rol):
        if not isinstance(rol, str) or rol not in cls.ROLES:
            raise ValueError(f"Rol no permitido. Debe ser uno de: {', '.join(cls.ROLES)}")
        return rol

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
        self._password_hash = texto_no_vacio(valor, "La contraseña")

    @classmethod
    def es_hash_bcrypt(cls, valor):
        return isinstance(valor, str) and cls._PATRON_HASH_BCRYPT.fullmatch(valor) is not None

    @classmethod
    def es_hash_sha256(cls, valor):
        return isinstance(valor, str) and cls._PATRON_HASH_SHA256.fullmatch(valor) is not None

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        self._rol = self.validar_rol(valor)

    def verificar_password(self, clave_ingresada: str) -> bool:
        """Comprueba bcrypt y, temporalmente, formatos heredados hasta su migración."""
        if not isinstance(clave_ingresada, str):
            return False
        clave_bytes = clave_ingresada.encode("utf-8")
        if not clave_bytes:
            return False
        if self.es_hash_bcrypt(self.password_hash):
            return (
                len(clave_bytes) <= self.MAX_BYTES_BCRYPT
                and bcrypt.checkpw(clave_bytes, self.password_hash.encode("utf-8"))
            )
        if self.es_hash_sha256(self.password_hash):
            hash_ingresado = hashlib.sha256(clave_bytes).hexdigest()
            return hmac.compare_digest(hash_ingresado, self.password_hash.lower())
        return hmac.compare_digest(clave_bytes, self.password_hash.encode("utf-8"))

    def mostrar_datos(self):
        return f"[{self.id}] Usuario: {self.nombre_usuario} (Rol: {self.rol}, Empleado ID: {self.empleado_id})"

    def __str__(self):
        return self.mostrar_datos()