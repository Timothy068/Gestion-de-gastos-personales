from datetime import datetime
from src.model.errors import CantidadNegativaError, TipoTransaccionInvalidoError, CategoriaInvalidaError, FechaFuturaError, UsuarioNoEncontradoError

class Transaccion:
    def __init__(self, id: int, cantidad: float, fecha: datetime, tipo: str, categoria, usuario):
        if cantidad < 0:
            raise CantidadNegativaError("El monto de la transacción no puede ser negativo")
        if tipo not in ["Ingreso", "Egreso"]:
            raise TipoTransaccionInvalidoError("El tipo de transacción debe ser 'Ingreso' o 'Egreso'")
        if not categoria:
            raise CategoriaInvalidaError("La categoría de la transacción no puede ser nula")
        if fecha > datetime.now():
            raise FechaFuturaError("La fecha de la transacción no puede estar en el futuro")
        if not usuario:
            raise UsuarioNoEncontradoError("El usuario de la transacción no puede ser nulo")
        
        self.id = id
        self.cantidad = cantidad
        self.fecha = fecha
        self.tipo = tipo
        self.categoria = categoria
        self.usuario = usuario

    def modificar_transaccion(self, nueva_cantidad=None, nueva_fecha=None, nuevo_tipo=None, nueva_categoria=None):
        if all(param is None for param in [nueva_cantidad, nueva_fecha, nuevo_tipo, nueva_categoria]):
            raise ValueError("Debe proporcionar al menos un parámetro para modificar la transacción")
        if nueva_cantidad is not None:
            if nueva_cantidad < 0:
                raise CantidadNegativaError("El monto de la transacción no puede ser negativo")
            self.cantidad = nueva_cantidad
        if nueva_fecha is not None:
            if nueva_fecha > datetime.now():
                raise FechaFuturaError("La fecha de la transacción no puede estar en el futuro")
            self.fecha = nueva_fecha
        if nuevo_tipo is not None:
            if nuevo_tipo not in ["Ingreso", "Egreso"]:
                raise TipoTransaccionInvalidoError("El tipo de transacción debe ser 'Ingreso' o 'Egreso'")
            self.tipo = nuevo_tipo
        if nueva_categoria is not None:
            if not nueva_categoria:
                raise CategoriaInvalidaError("La categoría de la transacción no puede ser nula")
            self.categoria = nueva_categoria

    def ver_transacciones(self):
        return {
            "id": self.id,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
            "tipo": self.tipo,
            "categoria": self.categoria,
            "usuario": self.usuario
        }

    def ver_detalle(self):
        return f"Transacción {self.id}: {self.tipo} de {self.cantidad} en {self.categoria.nombre} el {self.fecha}"
