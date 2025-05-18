import re
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base
from src.model.errors import CorreoInvalidoError, ContrasenaInseguraError, CamposVaciosError

Base = declarative_base()

class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Registro(id={self.id}, nombre={self.nombre}, correo={self.correo})>"

    @validates('nombre', 'correo', 'contrasena')
    def validate_fields(self, key, value):
        if not value:
            raise CamposVaciosError(f"El campo {key} es obligatorio")

        if key == "correo":
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                raise CorreoInvalidoError("El formato del correo es inválido")

        if key == "contrasena":
            if len(value) < 8:
                raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")

        return value

    def establecer_datos_personales(self, nombre: str, correo: str):
        self.nombre = nombre
        self.correo = correo

    def establecer_contrasena(self, contrasena: str):
        self.contrasena = contrasena
