from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from datetime import datetime

from src.model.usuario import Usuario
from src.model.categoria import Categoria
from src.model.transaccion import Transaccion
from src.model.errors import ContrasenaIncorrectaError, CorreoInvalidoError
from src.model.sesion import Sesion

from src.model.db import SessionLocal


class MenuApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.title_label = Label(
            text="Gestor de Gastos Personales",
            font_size=30,
            bold=True,
            color=(0.1, 0.6, 0.1, 1)
        )
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

        self.actualizar_usuario_label()

        return self.root

    def actualizar_usuario_label(self):
        usuario = Sesion.obtener_usuario_actual()
        self.usuario_label.text = f"Usuario en sesión: {usuario.nombre}" if usuario else "Usuario en sesión: Ninguno"

    def crear_usuario(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        nombre_input = TextInput()
        correo_input = TextInput()
        contrasena_input = TextInput(password=True)

        layout.add_widget(Label(text="Nombre:"))
        layout.add_widget(nombre_input)
        layout.add_widget(Label(text="Correo:"))
        layout.add_widget(correo_input)
        layout.add_widget(Label(text="Contraseña:"))
        layout.add_widget(contrasena_input)

        def on_submit(_):
            db = SessionLocal()
            try:
                # Validar que correo no exista
                existe = db.query(Usuario).filter(Usuario.correo == correo_input.text).first()
                if existe:
                    raise CorreoInvalidoError("El correo ya está registrado.")
                nuevo_usuario = Usuario(
                    nombre=nombre_input.text,
                    correo=correo_input.text,
                    contraseña=contrasena_input.text
                )
                db.add(nuevo_usuario)
                db.commit()
                db.refresh(nuevo_usuario)

                Sesion.iniciar_sesion(nuevo_usuario)
                popup.dismiss()
                self.actualizar_usuario_label()
                self.mostrar_popup("Usuario creado exitosamente.")
            except CorreoInvalidoError as e:
                self.mostrar_popup(str(e))
            except Exception as e:
                self.mostrar_popup(f"Error: {str(e)}")
            finally:
                db.close()

        submit_button = Button(text="Crear Usuario", size_hint_y=None, height=50)
        submit_button.bind(on_press=on_submit)
        layout.add_widget(submit_button)

        popup = Popup(title="Crear Usuario", content=layout, size_hint=(0.7, 0.6))
        popup.open()

    def iniciar_sesion(self, instance):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        correo_input = TextInput()
        contrasena_input = TextInput(password=True)

        layout.add_widget(Label(text="Correo:"))
        layout.add_widget(correo_input)
        layout.add_widget(Label(text="Contraseña:"))
        layout.add_widget(contrasena_input)

        def on_submit(_):
            db = SessionLocal()
            try:
                usuario = db.query(Usuario).filter(Usuario.correo == correo_input.text).first()
                if not usuario or usuario.contraseña != contrasena_input.text:
                    raise ContrasenaIncorrectaError()
                Sesion.iniciar_sesion(usuario)
                popup.dismiss()
                self.actualizar_usuario_label()
                self.mostrar_popup("Inicio de sesión exitoso.")
            except ContrasenaIncorrectaError:
                self.mostrar_popup("Correo o contraseña incorrectos.")
            except Exception as e:
                self.mostrar_popup(f"Error: {str(e)}")
            finally:
                db.close()

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
        cantidad_input = TextInput(input_filter='float')
        tipo_spinner = Spinner(text="Ingreso", values=["Ingreso", "Egreso"])
        categoria_spinner = Spinner(text="", values=[])

        def actualizar_categorias(tipo):
            db = SessionLocal()
            try:
                categorias_validas = db.query(Categoria).filter(Categoria.tipo == tipo).all()
                nombres = [c.nombre for c in categorias_validas]
                categoria_spinner.values = nombres
                if nombres:
                    categoria_spinner.text = nombres[0]
                else:
                    categoria_spinner.text = ""
            finally:
                db.close()

        # Inicializar categorías al abrir el popup
        actualizar_categorias(tipo_spinner.text)
        tipo_spinner.bind(text=lambda instance, value: actualizar_categorias(value))

        layout.add_widget(Label(text="Cantidad:"))
        layout.add_widget(cantidad_input)
        layout.add_widget(Label(text="Tipo:"))
        layout.add_widget(tipo_spinner)
        layout.add_widget(Label(text="Categoría:"))
        layout.add_widget(categoria_spinner)

        def on_submit(_):
            db = SessionLocal()
            try:
                cantidad = float(cantidad_input.text)
                tipo = tipo_spinner.text
                nombre_categoria = categoria_spinner.text
                if not nombre_categoria:
                    self.mostrar_popup("Debes seleccionar una categoría.")
                    return

                categoria = db.query(Categoria).filter(
                    Categoria.nombre == nombre_categoria,
                    Categoria.tipo == tipo
                ).first()
                if not categoria:
                    self.mostrar_popup("Categoría no válida.")
                    return

                nueva_transaccion = Transaccion(
                    cantidad=cantidad,
                    fecha=datetime.now(),
                    tipo=tipo,
                    categoria_id=categoria.id,
                    usuario_id=usuario.id
                )
                db.add(nueva_transaccion)
                db.commit()

                popup.dismiss()
                self.mostrar_popup("Transacción registrada exitosamente.")
            except ValueError:
                self.mostrar_popup("Cantidad inválida.")
            except Exception as e:
                self.mostrar_popup(f"Error: {str(e)}")
            finally:
                db.close()

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

        db = SessionLocal()
        try:
            transacciones = db.query(Transaccion).filter(
                Transaccion.usuario_id == usuario.id
            ).order_by(Transaccion.fecha.desc()).all()

            scroll_view = ScrollView(size_hint=(1, 1))
            layout = BoxLayout(orientation='vertical', size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))

            if not transacciones:
                layout.add_widget(Label(text="No hay transacciones para mostrar."))
            else:
                for t in transacciones:
                    # Accedemos a la categoría asociada para mostrar su nombre
                    categoria_nombre = t.categoria.nombre if t.categoria else "Sin categoría"
                    detalle = (f"ID: {t.id} | {t.tipo} | {t.cantidad} | "
                               f"{t.fecha.strftime('%Y-%m-%d %H:%M')} | Categoría: {categoria_nombre}")
                    layout.add_widget(Label(text=detalle, size_hint_y=None, height=30))

            scroll_view.add_widget(layout)
            popup = Popup(title="Transacciones", content=scroll_view, size_hint=(0.9, 0.9))
            popup.open()
        except Exception as e:
            self.mostrar_popup(f"Error: {str(e)}")
        finally:
            db.close()

    def eliminar_transaccion(self, instance):
        usuario = Sesion.obtener_usuario_actual()
        if not usuario:
            self.mostrar_popup("Debes iniciar sesión para eliminar una transacción.")
            return

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        id_input = TextInput(input_filter='int')

        layout.add_widget(Label(text="ID de la transacción a eliminar:"))
        layout.add_widget(id_input)

        def on_submit(_):
            db = SessionLocal()
            try:
                id_eliminar = int(id_input.text)
                transaccion = db.query(Transaccion).filter(
                    Transaccion.id == id_eliminar,
                    Transaccion.usuario_id == usuario.id
                ).first()
                if not transaccion:
                    self.mostrar_popup("Transacción no encontrada o no pertenece al usuario.")
                    return

                db.delete(transaccion)
                db.commit()
                popup.dismiss()
                self.mostrar_popup("Transacción eliminada exitosamente.")
            except ValueError:
                self.mostrar_popup("ID inválido.")
            except Exception as e:
                self.mostrar_popup(f"Error: {str(e)}")
            finally:
                db.close()

        submit_button = Button(text="Eliminar", size_hint_y=None, height=50)
        submit_button.bind(on_press=on_submit)
        layout.add_widget(submit_button)

        popup = Popup(title="Eliminar Transacción", content=layout, size_hint=(0.7, 0.6))
        popup.open()

    def cerrar_sesion(self, instance):
        Sesion.cerrar_sesion()
        self.actualizar_usuario_label()
        self.mostrar_popup("Sesión cerrada.")

    def mostrar_popup(self, mensaje):
        popup = Popup(title="Información", content=Label(text=mensaje), size_hint=(0.7, 0.5))
       
        popup.open()

