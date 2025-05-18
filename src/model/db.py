from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cambia estos datos según tu configuración
DATABASE_URL = "postgresql+psycopg2://postgres:Pepino2040@localhost:5432/gestion_gastosdb"

# Crear el engine de conexión con echo para ver las consultas SQL (útil para desarrollo)
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Base para los modelos (ORM)
Base = declarative_base()

# Crear sesión local para interacciones con la base de datos
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    """
    Generador para obtener la sesión de base de datos.
    Uso típico: 
        db = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
