class ErrorBase(Exception):
    """Clase base para errores personalizados en la aplicación."""
    pass

# Registro de transacción
class CantidadNegativaError(ErrorBase): pass
class TipoTransaccionInvalidoError(ErrorBase): pass
class CategoriaInvalidaError(ErrorBase): pass

# Actualización de transacción
class TransaccionNoEncontradaError(ErrorBase): pass
class FechaFuturaError(ErrorBase): pass

# Visualización de transacciones
class RangoFechasInvalidoError(ErrorBase): pass
class FechaInvalidaError(ErrorBase): pass

# Usuario
class UsuarioNoEncontradoError(ErrorBase): pass
class ContrasenaIncorrectaError(ErrorBase): pass
class CamposVaciosError(ErrorBase): pass

# Creación de cuenta
class CorreoYaRegistradoError(ErrorBase): pass
class ContrasenaInseguraError(ErrorBase): pass
class CorreoInvalidoError(ErrorBase): pass
