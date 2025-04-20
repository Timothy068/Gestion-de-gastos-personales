import re

class Categoria:
    """
    Representa una categoría dentro del sistema de gestión de gastos.
    """
    
    CATEGORIAS_VALIDAS_INGRESO = ["Salario", "Venta", "Otros", "General"]
    CATEGORIAS_VALIDAS_EGRESO = ["Alimentación", "Transporte", "Entretenimiento", "Salud", "Educación", "Otros", "General"]

    def __init__(self, id: int, nombre: str, descripcion: str):
        """
        Inicializa una nueva categoría.

        :param id: Identificador único de la categoría
        :param nombre: Nombre de la categoría (Ej. Alimentación, Transporte, etc.)
        :param descripcion: Descripción de la categoría
        :raises ValueError: Si alguno de los campos está vacío, el nombre es demasiado largo,
                            o contiene caracteres especiales no permitidos.
        """
        if not nombre or not descripcion:
            raise ValueError("El nombre y la descripción de la categoría son obligatorios.")
        if len(nombre) > 100:
            raise ValueError("El nombre de la categoría es demasiado largo. Máximo 100 caracteres.")
        if not re.match(r'^[\w\sáéíóúÁÉÍÓÚñÑ]+$', nombre):
            raise ValueError("El nombre de la categoría contiene caracteres no permitidos.")

        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    @staticmethod
    def obtener_categorias_validas_por_tipo(tipo):
        """Obtiene las categorías válidas dependiendo del tipo de transacción."""
        if tipo == "Ingreso":
            return Categoria.CATEGORIAS_VALIDAS_INGRESO
        elif tipo == "Egreso":
            return Categoria.CATEGORIAS_VALIDAS_EGRESO
        else:
            return []
