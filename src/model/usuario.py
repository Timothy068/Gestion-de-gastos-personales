import re
from src.model.errors import (
    ContrasenaIncorrectaError,
    CamposVaciosError,
    CorreoInvalidoError,
    ContrasenaInseguraError
)

class Usuario:
    """
    Representa a un usuario del sistema de gestión de gastos personales.
    """

    def __init__(self, id: int, nombre: str, correo: str, contraseña: str):
        """
        Inicializa un nuevo usuario con los datos básicos.

        :param id: Identificador único del usuario
        :param nombre: Nombre completo del usuario
        :param correo: Correo electrónico del usuario
        :param contraseña: Contraseña segura del usuario
        :raises CamposVaciosError: Si falta algún campo obligatorio
        :raises CorreoInvalidoError: Si el correo no tiene formato válido
        :raises ContrasenaInseguraError: Si la contraseña es demasiado corta
        """
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

    def iniciar_sesion(self, correo: str, contraseña: str) -> bool:
        """
        Valida las credenciales del usuario.

        :param correo: Correo electrónico ingresado
        :param contraseña: Contraseña ingresada
        :return: True si las credenciales coinciden
        :raises ContrasenaIncorrectaError: Si los datos no coinciden
        """
        if self.correo != correo or self.contraseña != contraseña:
            raise ContrasenaIncorrectaError("Correo o contraseña incorrectos")
        return True

    def cambiar_contraseña(self, nueva_contraseña: str):
        """
        Cambia la contraseña actual del usuario.

        :param nueva_contraseña: Nueva contraseña a establecer
        :raises ContrasenaInseguraError: Si la nueva contraseña no es segura
        """
        if len(nueva_contraseña) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")
        self.contraseña = nueva_contraseña
