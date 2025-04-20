import re
from src.model.errors import CorreoInvalidoError, ContrasenaInseguraError, CamposVaciosError

class Registro:
    """Gestiona el registro de cuentas de usuario."""

    def __init__(self, registro_id: int, nombre: str, correo: str):
        """
        Inicializa los datos de registro.

        Args:
            registro_id (int): ID único del registro.
            nombre (str): Nombre del usuario.
            correo (str): Correo electrónico del usuario.
        """
        self.id = registro_id
        self.nombre = nombre
        self.correo = correo
        self.contrasena = None

    def establecer_datos_personales(self, nombre: str, correo: str):
        """
        Valida e ingresa nombre y correo del usuario.

        Raises:
            CamposVaciosError: Si los campos están vacíos.
            CorreoInvalidoError: Si el formato del correo es incorrecto.
        """
        if not nombre or not correo:
            raise CamposVaciosError("El nombre y el correo son obligatorios")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise CorreoInvalidoError("El formato del correo es inválido")
        self.nombre = nombre
        self.correo = correo

    def establecer_contrasena(self, contrasena: str):
        """
        Valida y asigna una contraseña segura.

        Raises:
            CamposVaciosError: Si está vacía.
            ContrasenaInseguraError: Si tiene menos de 8 caracteres.
        """
        if not contrasena:
            raise CamposVaciosError("La contraseña es obligatoria")
        if len(contrasena) < 8:
            raise ContrasenaInseguraError("La contraseña debe tener al menos 8 caracteres")
        self.contrasena = contrasena
