import re
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from src.model.base import Base
import bcrypt

from src.model.errors import (
    ContrasenaIncorrectaError,
    CamposVaciosError,
    CorreoInvalidoError,
    ContrasenaInseguraError
)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)  # guardamos el hash aquí

    def __init__(self, nombre: str, correo: str, contraseña: str, id= None):
        if not nombre or not correo or not contraseña:
            raise CamposVaciosError("Todos los campos son obligatorios")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise CorreoInvalidoError("El formato del correo es inválido")
        if len(contraseña) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")

        self.nombre = nombre
        self.correo = correo
        self.contraseña = self._hash_password(contraseña)

    @validates("correo")
    def validar_correo(self, key, correo):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise CorreoInvalidoError("El formato del correo es inválido")
        return correo

    @validates("contraseña")
    def validar_contrasena(self, key, contraseña):
        if len(contraseña) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")
        return contraseña

    def _hash_password(self, contraseña: str) -> str:
        # Hashear la contraseña usando bcrypt y devolver en formato string utf-8
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(contraseña.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verificar_contraseña(self, contraseña: str) -> bool:
        # Verifica si la contraseña dada coincide con el hash guardado
        return bcrypt.checkpw(contraseña.encode("utf-8"), self.contraseña.encode("utf-8"))

    def iniciar_sesion(self, correo: str, contraseña: str) -> bool:
        if self.correo != correo or not self.verificar_contraseña(contraseña):
            raise ContrasenaIncorrectaError("Correo o contraseña incorrectos")
        return True

    def cambiar_contraseña(self, nueva_contraseña: str):
        if len(nueva_contraseña) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")
        self.contraseña = self._hash_password(nueva_contraseña)
