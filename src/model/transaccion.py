from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, validates, Session
import enum

from src.model.base import Base
from src.model.categoria import Categoria

class TipoTransaccionEnum(enum.Enum):
    INGRESO = "Ingreso"
    EGRESO = "Egreso"

class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    tipo = Column(Enum(TipoTransaccionEnum), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    categoria = relationship("Categoria")
    usuario = relationship("Usuario")

    def __init__(self, cantidad, fecha, tipo, categoria, usuario, session: Session, id=None):
        self._validar_datos_iniciales(cantidad, tipo, categoria, fecha, usuario, session)
        self.id = id
        self.cantidad = cantidad
        self.fecha = fecha

        if isinstance(tipo, str):
            tipo = tipo.capitalize()
            if tipo == "Ingreso":
                self.tipo = TipoTransaccionEnum.INGRESO
            elif tipo == "Egreso":
                self.tipo = TipoTransaccionEnum.EGRESO
            else:
                raise ValueError("Tipo debe ser 'Ingreso' o 'Egreso'")
        else:
            self.tipo = tipo

        self.categoria = categoria
        self.usuario = usuario

    def _validar_datos_iniciales(self, cantidad, tipo, categoria, fecha, usuario, session: Session):
        tipo_str = tipo.value if isinstance(tipo, TipoTransaccionEnum) else tipo.capitalize()

        if cantidad < 0:
            raise ValueError("El monto de la transacción no puede ser negativo")
        if tipo_str not in ["Ingreso", "Egreso"]:
            raise ValueError("Tipo debe ser 'Ingreso' o 'Egreso'")

        categorias_en_db = session.query(Categoria).filter(Categoria.tipo == tipo_str).all()
        categorias_validas = [cat.nombre for cat in categorias_en_db]

        nombre_categoria = categoria.nombre if hasattr(categoria, "nombre") else categoria

        if nombre_categoria not in categorias_validas:
            raise ValueError(f"Categoría '{nombre_categoria}' no válida para tipo '{tipo_str}'")

        if fecha > datetime.now():
            raise ValueError("La fecha no puede ser futura")
        if not usuario:
            raise ValueError("Usuario no válido")

    @validates("cantidad")
    def validar_cantidad(self, key, value):
        if value < 0:
            raise ValueError("La cantidad no puede ser negativa")
        return value

    @validates("fecha")
    def validar_fecha(self, key, value):
        if value > datetime.now():
            raise ValueError("No se permite una fecha futura")
        return value

    @validates("tipo")
    def validar_tipo(self, key, value):
        if value.value not in ["Ingreso", "Egreso"]:
            raise ValueError("Tipo no válido")
        return value

    def modificar_cantidad(self, nueva_cantidad: float):
        self.cantidad = nueva_cantidad

    def modificar_fecha(self, nueva_fecha: datetime):
        self.fecha = nueva_fecha

    def modificar_tipo(self, nuevo_tipo: str):
        nuevo_tipo_cap = nuevo_tipo.capitalize()
        if nuevo_tipo_cap not in ["Ingreso", "Egreso"]:
            raise ValueError("Tipo no válido")
        self.tipo = TipoTransaccionEnum[nuevo_tipo.upper()]

    def modificar_categoria(self, nueva_categoria):
        self.categoria = nueva_categoria

    def obtener_datos(self):
        return {
            "id": self.id,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
            "tipo": self.tipo.value,
            "categoria": self.categoria.nombre if self.categoria else None,
            "usuario": self.usuario.id if self.usuario else None
        }

    def ver_detalle(self):
        nombre_categoria = self.categoria.nombre if self.categoria else "Sin categoría"
        return f"Transacción {self.id}: {self.tipo.value} de {self.cantidad} en {nombre_categoria} el {self.fecha}"

    def modificar_transaccion(self, nueva_cantidad=None, nueva_fecha=None, nuevo_tipo=None, nueva_categoria=None):
        if (
            nueva_cantidad is None and
            nueva_fecha is None and
            nuevo_tipo is None and
            nueva_categoria is None
        ):
            raise ValueError("Debe proporcionar al menos un dato para modificar.")

        if nueva_cantidad is not None:
            self.modificar_cantidad(nueva_cantidad)
        if nueva_fecha is not None:
            self.modificar_fecha(nueva_fecha)
        if nuevo_tipo is not None:
            self.modificar_tipo(nuevo_tipo)
        if nueva_categoria is not None:
            self.modificar_categoria(nueva_categoria)
