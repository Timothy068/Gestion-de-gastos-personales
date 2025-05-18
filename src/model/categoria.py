from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.orm import validates
import enum
import re
from src.model.base import Base  # Importa Base desde base.py

class TipoCategoria(enum.Enum):
    INGRESO = "Ingreso"
    EGRESO = "Egreso"

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    tipo = Column(Enum(TipoCategoria), nullable=False)
    descripcion = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre={self.nombre}, tipo={self.tipo.value}, descripcion={self.descripcion})>"

    @validates('nombre')
    def validate_nombre(self, key, nombre):
        if not nombre:
            raise ValueError("El nombre de la categoría es obligatorio.")
        if len(nombre) > 100:
            raise ValueError("El nombre de la categoría es demasiado largo. Máximo 100 caracteres.")
        if not re.match(r'^[\w\sáéíóúÁÉÍÓÚñÑ]+$', nombre):
            raise ValueError("El nombre de la categoría contiene caracteres no permitidos.")
        return nombre

    @validates('tipo')
    def validate_tipo(self, key, tipo):
        if isinstance(tipo, str):
            try:
                tipo = TipoCategoria[tipo.upper()]
            except KeyError:
                raise ValueError("El tipo de categoría debe ser 'Ingreso' o 'Egreso'.")
        if not isinstance(tipo, TipoCategoria):
            raise ValueError("El tipo de categoría debe ser 'Ingreso' o 'Egreso'.")
        return tipo

    @validates('descripcion')
    def validate_descripcion(self, key, descripcion):
        if descripcion and len(descripcion) > 500:
            raise ValueError("La descripción es demasiado larga. Máximo 500 caracteres.")
        return descripcion

    @staticmethod
    def categorias_por_tipo(tipo_str):
        if tipo_str.lower() == "ingreso":
            return [
                ("Salario", "Dinero recibido por trabajo."),
                ("Venta", "Ingresos por ventas de productos o servicios."),
                ("Otros", "Otros ingresos varios."),
                ("General", "Categoría general para ingresos no especificados.")
            ]
        elif tipo_str.lower() == "egreso":
            return [
                ("Alimentación", "Gastos en comida y bebida."),
                ("Transporte", "Gastos en transporte público o vehículo."),
                ("Entretenimiento", "Gastos en ocio y diversión."),
                ("Salud", "Gastos médicos y de salud."),
                ("Educación", "Gastos en estudios y cursos."),
                ("Otros", "Otros gastos varios."),
                ("General", "Categoría general para egresos no especificados.")
            ]
        return []
