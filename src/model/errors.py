class ErrorBase(Exception):
    """Clase base para los errores personalizados"""
    pass

# ---- Errores de Registro de Transacción ----
class CantidadNegativaError(ErrorBase):
    """Se lanza cuando el monto de una transacción es negativo"""
    pass

class TipoTransaccionInvalidoError(ErrorBase):
    """Se lanza cuando el tipo de transacción no es 'Ingreso' o 'Egreso'"""
    pass

class CategoriaInvalidaError(ErrorBase):
    """Se lanza cuando la categoría de una transacción es inválida"""
    pass

# ---- Errores de Actualización de Transacción ----
class TransaccionNoEncontradaError(ErrorBase):
    """Se lanza cuando se intenta actualizar una transacción inexistente"""
    pass

class FechaFuturaError(ErrorBase):
    """Se lanza cuando se intenta registrar o actualizar una transacción con una fecha futura"""
    pass

# ---- Errores de Visualización de Transacciones ----
class RangoFechasInvalidoError(ErrorBase):
    """Se lanza cuando la fecha de inicio es posterior a la fecha de fin"""
    pass

class FechaInvalidaError(ErrorBase):
    """Se lanza cuando el formato de la fecha es incorrecto"""
    pass

# ---- Errores de Usuario ----
class UsuarioNoEncontradoError(ErrorBase):
    """Se lanza cuando el usuario no existe en el sistema"""
    pass

class ContrasenaIncorrectaError(ErrorBase):
    """Se lanza cuando la contraseña ingresada no es válida"""
    pass

class CamposVaciosError(ErrorBase):
    """Se lanza cuando falta información obligatoria al crear un usuario"""
    pass

# ---- Errores de Creación de Cuenta ----
class CorreoYaRegistradoError(ErrorBase):
    """Se lanza cuando se intenta registrar un correo ya existente"""
    pass

class ContrasenaInseguraError(ErrorBase):
    """Se lanza cuando la contraseña no cumple con los requisitos mínimos"""
    pass
