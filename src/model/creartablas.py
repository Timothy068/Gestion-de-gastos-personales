import psycopg2

def crear_tablas():
    comandos = [
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        );
        """,
        """
       CREATE TABLE IF NOT EXISTS categorias (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE NOT NULL,
            tipo VARCHAR(20) NOT NULL DEFAULT 'Ingreso' CHECK (tipo IN ('Ingreso', 'Egreso'))
            );
            '
            
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS transacciones (
            id SERIAL PRIMARY KEY,
            cantidad NUMERIC(10,2) NOT NULL,
            tipo TEXT CHECK(tipo IN ('ingreso', 'egreso')) NOT NULL,
            categoria_id INTEGER REFERENCES categorias(id),
            fecha TIMESTAMP NOT NULL,
            usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS registros (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
            actividad TEXT NOT NULL,
            fecha TIMESTAMP NOT NULL
        );
        """
    ]

    try:
        # Conecta a la base de datos (ajusta los parámetros)
        conexion = psycopg2.connect(
            host="127.0.0.1",
            database="gestion_gastosdb",
            user="postgres",
            password="Pepino2040"
        )
        cursor = conexion.cursor()

        for comando in comandos:
            cursor.execute(comando)

        conexion.commit()
        print("Tablas creadas correctamente.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

if __name__ == "__main__":
    crear_tablas()
