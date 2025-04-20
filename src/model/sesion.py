
class Sesion:
    _usuario_actual = None

    @classmethod
    def iniciar_sesion(cls, usuario):
        cls._usuario_actual = usuario

    @classmethod
    def cerrar_sesion(cls):
        cls._usuario_actual = None

    @classmethod
    def obtener_usuario_actual(cls):
        return cls._usuario_actual
