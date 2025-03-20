import re
from src.model.errors import CorreoInvalidoError, ContrasenaInseguraError, CamposVaciosError

class Registros:
    def __init__(self, id: int, nombre: str, correo: str):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.contraseña = None

    def crear_cuenta(self, nombre: str, correo: str):
        if not nombre or not correo:
            raise CamposVaciosError("El nombre y el correo son obligatorios")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise CorreoInvalidoError("El formato del correo es inválido")
        self.nombre = nombre
        self.correo = correo

    def crear_contraseña(self, contraseña: str):
        if not contraseña:
            raise CamposVaciosError("La contraseña es obligatoria")
        if len(contraseña) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")
        self.contraseña = contraseña
