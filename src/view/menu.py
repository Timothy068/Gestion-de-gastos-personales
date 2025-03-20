from src.model.usuario import Usuario
from src.model.categoria import Categoria
from src.model.transaccion import Transaccion
from src.model.registros import Registros
from src.model.errors import ContrasenaIncorrectaError
from datetime import datetime, timedelta

def mostrar_menu():
    print("1. Crear Usuario")
    print("2. Iniciar Sesión")
    print("3. Registrar Transacción")
    print("4. Visualizar Transacciones")
    print("5. Actualizar Transacción")
    print("6. Eliminar Transacción")
    print("7. Salir")

def crear_usuario():
    nombre = input("Ingrese su nombre: ")
    correo = input("Ingrese su correo: ")
    contraseña = input("Ingrese su contraseña: ")
    usuario = Usuario(id=1, nombre=nombre, correo=correo, contraseña=contraseña)
    print(f"Usuario {usuario.nombre} creado exitosamente.")

def iniciar_sesion():
    correo = input("Ingrese su correo: ")
    contraseña = input("Ingrese su contraseña: ")
    usuario = Usuario(id=1, nombre="Juan", correo=correo, contraseña=contraseña)
    try:
        usuario.iniciar_sesion(correo, contraseña)
        print("Inicio de sesión exitoso.")
    except ContrasenaIncorrectaError:
        print("Correo o contraseña incorrectos.")

def registrar_transaccion():
    cantidad = float(input("Ingrese la cantidad: "))
    fecha = datetime.now()
    tipo = input("Ingrese el tipo (Ingreso/Egreso): ")
    categoria = Categoria(id=1, nombre="General", descripcion="Gastos generales")
    usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")
    transaccion = Transaccion(id=1, cantidad=cantidad, fecha=fecha, tipo=tipo, categoria=categoria, usuario=usuario)
    print(f"Transacción de {transaccion.cantidad} registrada exitosamente.")

def visualizar_transacciones():
    transacciones = [
        Transaccion(id=1, cantidad=100.0, fecha=datetime.now() - timedelta(days=5), tipo="Ingreso", categoria=Categoria(id=1, nombre="General", descripcion="Gastos generales"), usuario=Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")),
        Transaccion(id=2, cantidad=50.0, fecha=datetime.now() - timedelta(days=3), tipo="Egreso", categoria=Categoria(id=1, nombre="General", descripcion="Gastos generales"), usuario=Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")),
        Transaccion(id=3, cantidad=200.0, fecha=datetime.now(), tipo="Ingreso", categoria=Categoria(id=1, nombre="General", descripcion="Gastos generales"), usuario=Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123"))
    ]
    for transaccion in transacciones:
        print(transaccion.ver_detalle())

def actualizar_transaccion():
    transaccion_id = int(input("Ingrese el ID de la transacción a actualizar: "))
    nueva_cantidad = float(input("Ingrese la nueva cantidad: "))
    nueva_fecha = datetime.now()
    nuevo_tipo = input("Ingrese el nuevo tipo (Ingreso/Egreso): ")
    nueva_categoria = Categoria(id=2, nombre="Transporte", descripcion="Gastos en transporte")
    transaccion = Transaccion(id=transaccion_id, cantidad=nueva_cantidad, fecha=nueva_fecha, tipo=nuevo_tipo, categoria=nueva_categoria, usuario=Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123"))
    transaccion.modificar_transaccion(nueva_cantidad=nueva_cantidad, nueva_fecha=nueva_fecha, nuevo_tipo=nuevo_tipo, nueva_categoria=nueva_categoria)
    print(f"Transacción {transaccion.id} actualizada exitosamente.")

def eliminar_transaccion():
    transaccion_id = int(input("Ingrese el ID de la transacción a eliminar: "))
    # Aquí se debería implementar la lógica para eliminar la transacción
    print(f"Transacción {transaccion_id} eliminada exitosamente.")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            registrar_transaccion()
        elif opcion == "4":
            visualizar_transacciones()
        elif opcion == "5":
            actualizar_transaccion()
        elif opcion == "6":
            eliminar_transaccion()
        elif opcion == "7":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
