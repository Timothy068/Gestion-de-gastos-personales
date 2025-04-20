from datetime import datetime
from src.model.categoria import Categoria
from src.model.errors import (
    CantidadNegativaError,
    TipoTransaccionInvalidoError,
    CategoriaInvalidaError,
    FechaFuturaError,
    UsuarioNoEncontradoError
)

class Transaccion:
    """Representa una transacción financiera de ingreso o egreso."""

    def __init__(self, id: int, cantidad: float, fecha: datetime, tipo: str, categoria, usuario):
        """
        Inicializa una transacción con sus datos básicos y validaciones.

        Args:
            id (int): ID único.
            cantidad (float): Monto de la transacción.
            fecha (datetime): Fecha de la transacción.
            tipo (str): Tipo 'Ingreso' o 'Egreso'.
            categoria (Categoria): Objeto de categoría.
            usuario (Usuario): Usuario relacionado.
        """
        self._validar_datos_iniciales(cantidad, tipo, categoria, fecha, usuario)
        self.id = id
        self.cantidad = cantidad
        self.fecha = fecha
        self.tipo = tipo
        self.categoria = categoria
        self.usuario = usuario

    def _validar_datos_iniciales(self, cantidad, tipo, categoria, fecha, usuario):
        """Valida los datos iniciales para la transacción."""
        if cantidad < 0:
            raise CantidadNegativaError("El monto de la transacción no puede ser negativo")
        if tipo not in ["Ingreso", "Egreso"]:
            raise TipoTransaccionInvalidoError("Tipo debe ser 'Ingreso' o 'Egreso'")

        # Validación de categoría según tipo usando el método estático
        categorias_validas = Categoria.obtener_categorias_validas_por_tipo(tipo)

        # Verificar si la categoría es válida
        if isinstance(categoria, str):
            if categoria not in categorias_validas:
                raise CategoriaInvalidaError("Categoría no válida para este tipo de transacción")
        elif hasattr(categoria, 'nombre'):
            if categoria.nombre not in categorias_validas:
                raise CategoriaInvalidaError("Categoría no válida para este tipo de transacción")
        else:
            raise CategoriaInvalidaError("Categoría inválida")

        if fecha > datetime.now():
            raise FechaFuturaError("La fecha no puede ser futura")
        if not usuario:
            raise UsuarioNoEncontradoError("Usuario no válido")

    def modificar_cantidad(self, nueva_cantidad: float):
        """Modifica la cantidad de la transacción."""
        if nueva_cantidad < 0:
            raise CantidadNegativaError("La cantidad no puede ser negativa")
        self.cantidad = nueva_cantidad

    def modificar_fecha(self, nueva_fecha: datetime):
        """Modifica la fecha de la transacción."""
        if nueva_fecha > datetime.now():
            raise FechaFuturaError("No se permite una fecha futura")
        self.fecha = nueva_fecha

    def modificar_tipo(self, nuevo_tipo: str):
        """Modifica el tipo de la transacción (Ingreso/Egreso)."""
        if nuevo_tipo not in ["Ingreso", "Egreso"]:
            raise TipoTransaccionInvalidoError("Tipo no válido")
        self.tipo = nuevo_tipo

    def modificar_categoria(self, nueva_categoria):
        """Modifica la categoría de la transacción."""
        # Validación por tipo de transacción usando el método estático
        categorias_validas = Categoria.obtener_categorias_validas_por_tipo(self.tipo)

        if isinstance(nueva_categoria, str):
            if nueva_categoria not in categorias_validas:
                raise CategoriaInvalidaError("Categoría inválida")
            self.categoria = Categoria(id=0, nombre=nueva_categoria, descripcion="")
        elif hasattr(nueva_categoria, 'nombre'):
            if nueva_categoria.nombre not in categorias_validas:
                raise CategoriaInvalidaError("Categoría inválida")
            self.categoria = nueva_categoria
        else:
            raise CategoriaInvalidaError("Categoría inválida")

    def obtener_datos(self):
        """Obtiene los datos de la transacción."""
        return {
            "id": self.id,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
            "tipo": self.tipo,
            "categoria": self.categoria.nombre if hasattr(self.categoria, 'nombre') else self.categoria,
            "usuario": self.usuario
        }

    def ver_detalle(self):
        """Obtiene el detalle de la transacción como una cadena."""
        nombre_categoria = self.categoria.nombre if hasattr(self.categoria, 'nombre') else str(self.categoria)
        return f"Transacción {self.id}: {self.tipo} de {self.cantidad} en {nombre_categoria} el {self.fecha}"

    def modificar_transaccion(self, nueva_cantidad=None, nueva_fecha=None, nuevo_tipo=None, nueva_categoria=None):
        """Permite modificar uno o más atributos de la transacción."""
        if nueva_cantidad is None and nueva_fecha is None and nuevo_tipo is None and nueva_categoria is None:
            raise ValueError("Debe proporcionar al menos un dato para modificar.")
    
        if nueva_cantidad is not None:
            self.modificar_cantidad(nueva_cantidad)
        if nueva_fecha is not None:
            self.modificar_fecha(nueva_fecha)
        if nuevo_tipo is not None:
            self.modificar_tipo(nuevo_tipo)
        if nueva_categoria is not None:
            # Validación por nombre de categoría usando el método estático
            categorias_validas = Categoria.obtener_categorias_validas_por_tipo(self.tipo)

            if isinstance(nueva_categoria, str):
                if nueva_categoria not in categorias_validas:
                    raise CategoriaInvalidaError("Categoría inválida")
                self.categoria = Categoria(id=0, nombre=nueva_categoria, descripcion="")
            elif hasattr(nueva_categoria, 'nombre'):
                if nueva_categoria.nombre not in categorias_validas:
                    raise CategoriaInvalidaError("Categoría inválida")
                self.categoria = nueva_categoria
            else:
                raise CategoriaInvalidaError("Categoría inválida")
