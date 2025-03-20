import re
from src.model.errors import ContrasenaIncorrectaError, CamposVaciosError, CorreoInvalidoError, ContrasenaInseguraError

class Usuario:
    def __init__(self, id: int, nombre: str, correo: str, contraseña: str):
        if not nombre or not correo or not contraseña:
            raise CamposVaciosError("Todos los campos son obligatorios")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise CorreoInvalidoError("El formato del correo es inválido")
        if len(contraseña) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña

    def iniciar_sesion(self, correo: str, contraseña: str):
        if self.correo != correo or self.contraseña != contraseña:
            raise ContrasenaIncorrectaError("Correo o contraseña incorrectos")
        return True

    def cambiar_contraseña(self, nueva_contraseña: str):
        if len(nueva_contraseña) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")
        self.contraseña = nueva_contraseña
