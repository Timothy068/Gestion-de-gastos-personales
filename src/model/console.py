from datetime import datetime
from src.model.usuario import Usuario
from src.model.categoria import Categoria
from src.model.transaccion import Transaccion
from src.model.errors import ContrasenaIncorrectaError, CorreoInvalidoError
from src.model.sesion import Sesion
from src.model.db import SessionLocal

def crear_usuario():
    print("\n=== Crear Usuario ===")
    nombre = input("Nombre: ").strip()
    correo = input("Correo: ").strip()
    contrasena = input("Contraseña: ").strip()

    db = SessionLocal()
    try:
        existe = db.query(Usuario).filter(Usuario.correo == correo).first()
        if existe:
            print("Error: El correo ya está registrado.")
            return
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, contraseña=contrasena)
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        Sesion.iniciar_sesion(nuevo_usuario)
        print(f"Usuario '{nombre}' creado y sesión iniciada.")
    except Exception as e:
        print(f"Error al crear usuario: {e}")
    finally:
        db.close()

def iniciar_sesion():
    print("\n=== Iniciar Sesión ===")
    correo = input("Correo: ").strip()
    contrasena = input("Contraseña: ").strip()

    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
        if not usuario or usuario.contraseña != contrasena:
            raise ContrasenaIncorrectaError()
        Sesion.iniciar_sesion(usuario)
        print(f"Sesión iniciada. Bienvenido {usuario.nombre}.")
    except ContrasenaIncorrectaError:
        print("Error: Correo o contraseña incorrectos.")
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
    finally:
        db.close()

def registrar_transaccion():
    usuario = Sesion.obtener_usuario_actual()
    if not usuario:
        print("Debes iniciar sesión para registrar una transacción.")
        return

    print("\n=== Registrar Transacción ===")
    cantidad_str = input("Cantidad: ").strip()
    tipo = input("Tipo (Ingreso/Egreso): ").strip().capitalize()
    if tipo not in ("Ingreso", "Egreso"):
        print("Tipo inválido. Debe ser 'Ingreso' o 'Egreso'.")
        return

    db = SessionLocal()
    try:
        categorias_validas = db.query(Categoria).filter(Categoria.tipo == tipo).all()
        if not categorias_validas:
            print(f"No hay categorías disponibles para tipo '{tipo}'.")
            return
        print("Categorías disponibles:")
        for idx, cat in enumerate(categorias_validas, 1):
            print(f"{idx}. {cat.nombre}")
        cat_idx_str = input("Selecciona número de categoría: ").strip()
        try:
            cat_idx = int(cat_idx_str)
            if not (1 <= cat_idx <= len(categorias_validas)):
                print("Número de categoría inválido.")
                return
        except ValueError:
            print("Entrada inválida para número de categoría.")
            return
        categoria = categorias_validas[cat_idx - 1]

        cantidad = float(cantidad_str)
        nueva_transaccion = Transaccion(
            cantidad=cantidad,
            fecha=datetime.now(),
            tipo=tipo,
            categoria_id=categoria.id,
            usuario_id=usuario.id
        )
        db.add(nueva_transaccion)
        db.commit()
        print("Transacción registrada exitosamente.")
    except ValueError:
        print("Cantidad inválida.")
    except Exception as e:
        print(f"Error al registrar transacción: {e}")
    finally:
        db.close()

def visualizar_transacciones():
    usuario = Sesion.obtener_usuario_actual()
    if not usuario:
        print("Debes iniciar sesión para visualizar transacciones.")
        return

    db = SessionLocal()
    try:
        transacciones = db.query(Transaccion).filter(Transaccion.usuario_id == usuario.id).order_by(Transaccion.fecha.desc()).all()
        print("\n=== Transacciones ===")
        if not transacciones:
            print("No hay transacciones para mostrar.")
            return
        for t in transacciones:
            categoria_nombre = t.categoria.nombre if t.categoria else "Sin categoría"
            detalle = (f"ID: {t.id} | {t.tipo} | {t.cantidad} | "
                       f"{t.fecha.strftime('%Y-%m-%d %H:%M')} | Categoría: {categoria_nombre}")
            print(detalle)
    except Exception as e:
        print(f"Error al visualizar transacciones: {e}")
    finally:
        db.close()

def eliminar_transaccion():
    usuario = Sesion.obtener_usuario_actual()
    if not usuario:
        print("Debes iniciar sesión para eliminar una transacción.")
        return

    print("\n=== Eliminar Transacción ===")
    id_str = input("ID de la transacción a eliminar: ").strip()

    db = SessionLocal()
    try:
        id_eliminar = int(id_str)
        transaccion = db.query(Transaccion).filter(Transaccion.id == id_eliminar, Transaccion.usuario_id == usuario.id).first()
        if not transaccion:
            print("Transacción no encontrada o no pertenece al usuario.")
            return
        db.delete(transaccion)
        db.commit()
        print("Transacción eliminada exitosamente.")
    except ValueError:
        print("ID inválido.")
    except Exception as e:
        print(f"Error al eliminar transacción: {e}")
    finally:
        db.close()

def cerrar_sesion():
    Sesion.cerrar_sesion()
    print("Sesión cerrada.")

def mostrar_menu():
    while True:
        usuario = Sesion.obtener_usuario_actual()
        nombre_usuario = usuario.nombre if usuario else "Ninguno"
        print(f"\n--- Gestor de Gastos Personales ---\nUsuario en sesión: {nombre_usuario}")
        print("1. Crear Usuario")
        print("2. Iniciar Sesión")
        print("3. Registrar Transacción")
        print("4. Visualizar Transacciones")
        print("5. Eliminar Transacción")
        print("6. Cerrar Sesión")
        print("7. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            registrar_transaccion()
        elif opcion == "4":
            visualizar_transacciones()
        elif opcion == "5":
            eliminar_transaccion()
        elif opcion == "6":
            cerrar_sesion()
        elif opcion == "7":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu()
