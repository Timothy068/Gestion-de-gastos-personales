from src.view.menu import mostrar_menu, crear_usuario, iniciar_sesion, registrar_transaccion, visualizar_transacciones, actualizar_transaccion, eliminar_transaccion

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
