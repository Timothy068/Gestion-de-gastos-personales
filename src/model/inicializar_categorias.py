import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.model.db import SessionLocal
from src.model.categoria import Categoria

db = SessionLocal()
categoria1 = Categoria(nombre="Salario", tipo="Ingreso")
categoria2 = Categoria(nombre="Comida", tipo="Egreso")
db.add(categoria1)
db.add(categoria2)
db.commit()
db.close()
