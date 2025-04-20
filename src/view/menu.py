from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from datetime import datetime, timedelta

from src.model.usuario import Usuario
from src.model.categoria import Categoria
from src.model.transaccion import Transaccion
from src.model.registros import Registro
from src.model.errors import ContrasenaIncorrectaError, CorreoInvalidoError
from src.model.sesion import Sesion

class MenuApp(App):
    def build(self):
        self.transacciones = []  # almacenamiento en memoria
        self.root = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title_label = Label(text="Gestor de Gastos Personales", font_size=30, bold=True, color=(0.1, 0.6, 0.1, 1))
        self.root.add_widget(self.title_label)

        self.boton_crear_usuario = Button(text="Crear Usuario", size_hint_y=None, height=50)
        self.boton_crear_usuario.bind(on_press=self.crear_usuario)
        self.root.add_widget(self.boton_crear_usuario)

        self.boton_iniciar_sesion = Button(text="Iniciar Sesión", size_hint_y=None, height=50)
        self.boton_iniciar_sesion.bind(on_press=self.iniciar_sesion)
        self.root.add_widget(self.boton_iniciar_sesion)

        self.boton_registrar_transaccion = Button(text="Registrar Transacción", size_hint_y=None, height=50)
        self.boton_registrar_transaccion.bind(on_press=self.registrar_transaccion)
        self.root.add_widget(self.boton_registrar_transaccion)

        self.boton_visualizar_transacciones = Button(text="Visualizar Transacciones", size_hint_y=None, height=50)
        self.boton_visualizar_transacciones.bind(on_press=self.visualizar_transacciones)
        self.root.add_widget(self.boton_visualizar_transacciones)

        self.boton_eliminar_transaccion = Button(text="Eliminar Transacción", size_hint_y=None, height=50)
        self.boton_eliminar_transaccion.bind(on_press=self.eliminar_transaccion)
        self.root.add_widget(self.boton_eliminar_transaccion)

        self.boton_cerrar_sesion = Button(text="Cerrar Sesión", size_hint_y=None, height=50)
        self.boton_cerrar_sesion.bind(on_press=self.cerrar_sesion)
        self.root.add_widget(self.boton_cerrar_sesion)

        self.usuario_label = Label(text="Usuario en sesión: Ninguno", font_size=14)
        self.root.add_widget(self.usuario_label)

        return self.root

    def actualizar_usuario_label(self):
        usuario = Sesion.obtener_usuario_actual()
        self.usuario_label.text = f"Usuario en sesión: {usuario.nombre}" if usuario else "Usuario en sesión: Ninguno"

    def crear_usuario(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        nombre_input, correo_input, contrasena_input = TextInput(), TextInput(), TextInput(password=True)
        layout.add_widget(Label(text="Nombre:"))
        layout.add_widget(nombre_input)
        layout.add_widget(Label(text="Correo:"))
        layout.add_widget(correo_input)
        layout.add_widget(Label(text="Contraseña:"))
        layout.add_widget(contrasena_input)

        def on_submit(_):
            try:
                usuario = Usuario(id=len(self.transacciones)+1, nombre=nombre_input.text, correo=correo_input.text, contraseña=contrasena_input.text)
                Sesion.iniciar_sesion(usuario)
                popup.dismiss()
                self.actualizar_usuario_label()
                self.mostrar_popup("Usuario creado exitosamente.")
            except CorreoInvalidoError as e:
                popup.dismiss()
                self.mostrar_popup(str(e))

        submit_button = Button(text="Crear Usuario", size_hint_y=None, height=50)
        submit_button.bind(on_press=on_submit)
        layout.add_widget(submit_button)

        popup = Popup(title="Crear Usuario", content=layout, size_hint=(0.7, 0.6))
        popup.open()

    def iniciar_sesion(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        correo_input, contrasena_input = TextInput(), TextInput(password=True)
        layout.add_widget(Label(text="Correo:"))
        layout.add_widget(correo_input)
        layout.add_widget(Label(text="Contraseña:"))
        layout.add_widget(contrasena_input)

        def on_submit(_):
            try:
                usuario = Usuario(id=1, nombre="Usuario", correo=correo_input.text, contraseña=contrasena_input.text)
                usuario.iniciar_sesion(correo_input.text, contrasena_input.text)
                Sesion.iniciar_sesion(usuario)
                popup.dismiss()
                self.actualizar_usuario_label()
                self.mostrar_popup("Inicio de sesión exitoso.")
            except ContrasenaIncorrectaError:
                popup.dismiss()
                self.mostrar_popup("Correo o contraseña incorrectos.")

        submit_button = Button(text="Iniciar Sesión", size_hint_y=None, height=50)
        submit_button.bind(on_press=on_submit)
        layout.add_widget(submit_button)

        popup = Popup(title="Iniciar Sesión", content=layout, size_hint=(0.7, 0.6))
        popup.open()

    def registrar_transaccion(self, instance):
        usuario = Sesion.obtener_usuario_actual()
        if not usuario:
            self.mostrar_popup("Debes iniciar sesión para registrar una transacción.")
            return

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        cantidad_input = TextInput()
        tipo_spinner = Spinner(text="Ingreso", values=["Ingreso", "Egreso"])
        categoria_spinner = Spinner(text="", values=[])

    # Se cambia aquí para obtener las categorías válidas según el tipo
        def actualizar_categorias(tipo):
            categorias_validas = Categoria.obtener_categorias_validas_por_tipo(tipo)
            categoria_spinner.values = categorias_validas
            categoria_spinner.text = categorias_validas[0] if categorias_validas else ""

    # Llamar a la función para actualizar las categorías según el tipo por defecto
        actualizar_categorias(tipo_spinner.text)

        tipo_spinner.bind(text=lambda instance, value: actualizar_categorias(value))

        layout.add_widget(Label(text="Cantidad:"))
        layout.add_widget(cantidad_input)
        layout.add_widget(Label(text="Tipo:"))
        layout.add_widget(tipo_spinner)
        layout.add_widget(Label(text="Categoría:"))
        layout.add_widget(categoria_spinner)

        def on_submit(_):
            try:
                cantidad = float(cantidad_input.text)
                tipo = tipo_spinner.text
                nombre_categoria = categoria_spinner.text

                if not nombre_categoria:
                    self.mostrar_popup("Debes seleccionar una categoría.")
                    return

                descripcion_categoria = f"Categoría correspondiente a un {tipo.lower()}."

                categoria = Categoria(id=1, nombre=nombre_categoria, descripcion=descripcion_categoria)

                transaccion = Transaccion(
                    id=len(self.transacciones) + 1,
                    cantidad=cantidad,
                    fecha=datetime.now(),
                    tipo=tipo,
                    categoria=categoria,
                    usuario=usuario
                )

                self.transacciones.append(transaccion)
                popup.dismiss()
                self.mostrar_popup("Transacción registrada exitosamente.")

            except ValueError as ve:
                self.mostrar_popup(f"Error de validación: {str(ve)}")
            except Exception as e:
                self.mostrar_popup(f"Error: {str(e)}")
        
        submit_button = Button(text="Registrar", size_hint_y=None, height=50)
        submit_button.bind(on_press=on_submit)
        layout.add_widget(submit_button)

        popup = Popup(title="Registrar Transacción", content=layout, size_hint=(0.8, 0.7))
        popup.open()

    def visualizar_transacciones(self, instance):
        usuario = Sesion.obtener_usuario_actual()
        if not usuario:
            self.mostrar_popup("Debes iniciar sesión para visualizar transacciones.")
            return

        scroll_view = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation='vertical', size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for t in self.transacciones:
            if t.usuario.id == usuario.id:
                layout.add_widget(Label(text=t.ver_detalle()))

        scroll_view.add_widget(layout)
        popup = Popup(title="Transacciones", content=scroll_view, size_hint=(0.9, 0.9))
        popup.open()

    def eliminar_transaccion(self, instance):
        usuario = Sesion.obtener_usuario_actual()
        if not usuario:
            self.mostrar_popup("Debes iniciar sesión para eliminar transacciones.")
            return

        layout = BoxLayout(orientation='vertical', padding=10)
        trans_id_input = TextInput(hint_text="ID de transacción a eliminar")
        layout.add_widget(trans_id_input)

        def on_submit(_):
            try:
                trans_id = int(trans_id_input.text)
                transaccion = next((t for t in self.transacciones if t.id == trans_id and t.usuario.id == usuario.id), None)
                if transaccion:
                    self.transacciones.remove(transaccion)
                    popup.dismiss()
                    self.mostrar_popup("Transacción eliminada.")
                else:
                    self.mostrar_popup("Transacción no encontrada o no tienes permiso.")
            except Exception as e:
                self.mostrar_popup(f"Error: {str(e)}")

        submit_button = Button(text="Eliminar", size_hint_y=None, height=50)
        submit_button.bind(on_press=on_submit)
        layout.add_widget(submit_button)

        popup = Popup(title="Eliminar Transacción", content=layout, size_hint=(0.7, 0.5))
        popup.open()

    def cerrar_sesion(self, instance):
        Sesion.cerrar_sesion()
        self.actualizar_usuario_label()
        self.mostrar_popup("Sesión cerrada correctamente.")

    def mostrar_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        close_button = Button(text="Cerrar", size_hint_y=None, height=50)
        content.add_widget(close_button)

        popup = Popup(title="Información", content=content, size_hint=(0.7, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == "__main__":
    MenuApp().run()