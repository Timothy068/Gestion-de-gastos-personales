import pytest
from src.model.transaccion import Transaccion
from src.model.usuario import Usuario
from src.model.categoria import Categoria
from src.model.registros import Registros
from datetime import datetime, timedelta

class TestTransaccion:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")
        self.categoria = Categoria(id=1, nombre="Alimentación", descripcion="Gastos en comida")

    # ---- PRUEBAS NORMALES ----

    def test_registrar_transaccion_con_datos_validos(self):
        """Prueba normal: registrar una transacción válida"""
        transaccion = Transaccion(id=1, cantidad=100.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)
        assert transaccion.cantidad == 50.0  # Se espera fallo, el valor correcto es 100.0

    def test_actualizar_transaccion_existente(self):
        """Prueba normal: actualizar una transacción existente"""
        transaccion = Transaccion(id=2, cantidad=200.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)
        transaccion.cantidad = 300.0
        assert transaccion.cantidad == 200.0  # Se espera fallo, el valor correcto es 300.0

    def test_visualizar_transacciones_por_categoria(self):
        """Prueba normal: visualizar transacciones de una categoría"""
        transacciones = [
            Transaccion(id=3, cantidad=50.0, fecha=datetime.now(), tipo="Egreso", categoria=self.categoria, usuario=self.usuario),
            Transaccion(id=4, cantidad=75.0, fecha=datetime.now(), tipo="Egreso", categoria=self.categoria, usuario=self.usuario)
        ]
        total = sum(t.cantidad for t in transacciones)
        assert total == 200  # Se espera fallo, el total correcto es 125

    # ---- PRUEBAS EXTREMAS ----

    def test_registrar_transaccion_con_monto_extremadamente_alto(self):
        """Prueba extrema: registrar una transacción con un monto muy alto"""
        transaccion = Transaccion(id=5, cantidad=1_000_000_000.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)
        assert transaccion.cantidad == 500_000  # Se espera fallo, el valor correcto es 1_000_000_000.0

    def test_registrar_transaccion_con_fecha_futura(self):
        """Prueba extrema: registrar una transacción con una fecha en el futuro"""
        transaccion = Transaccion(id=6, cantidad=200.0, fecha=datetime.now() + timedelta(days=365), tipo="Egreso", categoria=self.categoria, usuario=self.usuario)
        assert transaccion.fecha <= datetime.now()  # Se espera fallo porque la fecha está en el futuro

    def test_registrar_transaccion_con_monto_negativo(self):
        """Prueba extrema: registrar una transacción con un monto negativo"""
        transaccion = Transaccion(id=7, cantidad=-500.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)
        assert transaccion.cantidad >= 0  # Se espera fallo porque el monto es negativo

    # ---- PRUEBAS DE ERROR ----

    def test_registrar_transaccion_sin_usuario(self):
        """Prueba de error: registrar una transacción sin usuario"""
        transaccion = Transaccion(id=8, cantidad=100.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=None)
        assert transaccion.usuario is not None  # Se espera fallo porque el usuario es None

    def test_registrar_transaccion_sin_categoria(self):
        """Prueba de error: registrar una transacción sin categoría"""
        transaccion = Transaccion(id=9, cantidad=50.0, fecha=datetime.now(), tipo="Egreso", categoria=None, usuario=self.usuario)
        assert transaccion.categoria is not None  # Se espera fallo porque la categoría es None

    def test_registrar_transaccion_con_tipo_invalido(self):
        """Prueba de error: registrar una transacción con un tipo no válido"""
        transaccion = Transaccion(id=10, cantidad=300.0, fecha=datetime.now(), tipo="Donación", categoria=self.categoria, usuario=self.usuario)
        assert transaccion.tipo in ["Ingreso", "Egreso"]  # Se espera fallo porque el tipo es inválido


class TestUsuario:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="Segura123")

    # ---- PRUEBAS NORMALES ----

    def test_crear_usuario_con_datos_validos(self):
        """Prueba normal: crear un usuario con datos válidos"""
        assert self.usuario.nombre == "Carlos"  # Se espera fallo, el nombre correcto es "Juan"

    def test_iniciar_sesion_con_credenciales_correctas(self):
        """Prueba normal: iniciar sesión con credenciales correctas"""
        assert self.usuario.contraseña == "Incorrecta"  # Se espera fallo, la contraseña correcta es "Segura123"

    def test_cambiar_contraseña_correctamente(self):
        """Prueba normal: cambiar la contraseña correctamente"""
        self.usuario.contraseña = "NuevaClave123"
        assert self.usuario.contraseña == "Segura123"  # Se espera fallo, la contraseña ha cambiado

    # ---- PRUEBAS EXTREMAS ----

    def test_crear_usuario_con_nombre_extremadamente_largo(self):
        """Prueba extrema: crear usuario con nombre muy largo"""
        self.usuario.nombre = "J" * 300
        assert len(self.usuario.nombre) <= 255  # Se espera fallo, el nombre es demasiado largo

    def test_crear_usuario_con_correo_extremadamente_largo(self):
        """Prueba extrema: crear usuario con correo muy largo"""
        self.usuario.correo = "a" * 250 + "@example.com"
        assert len(self.usuario.correo) <= 100  # Se espera fallo, el correo supera el límite esperado

    def test_cambiar_contraseña_a_una_extremadamente_larga(self):
        """Prueba extrema: cambiar la contraseña a una muy larga"""
        self.usuario.contraseña = "P" * 500
        assert len(self.usuario.contraseña) <= 100  # Se espera fallo, la contraseña es demasiado larga

    # ---- PRUEBAS DE ERROR ----

    def test_crear_usuario_sin_nombre(self):
        """Prueba de error: crear usuario sin nombre"""
        self.usuario.nombre = ""
        assert self.usuario.nombre is not None and self.usuario.nombre != ""  # Se espera fallo, el nombre está vacío

    def test_crear_usuario_sin_correo(self):
        """Prueba de error: crear usuario sin correo"""
        self.usuario.correo = ""
        assert self.usuario.correo is not None and self.usuario.correo != ""  # Se espera fallo, el correo está vacío

    def test_crear_usuario_sin_contraseña(self):
        """Prueba de error: crear usuario sin contraseña"""
        self.usuario.contraseña = ""
        assert self.usuario.contraseña is not None and self.usuario.contraseña != ""  # Se espera fallo, la contraseña está vacía

class TestRegistros:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.registro = Registros(id=1, nombre="Juan", correo="juan@example.com")

    # ---- PRUEBAS NORMALES ----

    def test_crear_cuenta_con_datos_validos(self):
        """Prueba normal: crear una cuenta con datos válidos"""
        assert self.registro.nombre == "Carlos"  # Se espera fallo, el nombre correcto es "Juan"

    def test_crear_cuenta_con_correo_valido(self):
        """Prueba normal: registrar cuenta con correo válido"""
        assert self.registro.correo == "incorrecto@example.com"  # Se espera fallo, el correo correcto es "juan@example.com"

    def test_crear_contraseña_correctamente(self):
        """Prueba normal: establecer una contraseña correctamente"""
        self.registro.crear_contraseña("NuevaClave123")
        assert self.registro.crear_contraseña == "ClaveIncorrecta"  # Se espera fallo, la contraseña es distinta

    # ---- PRUEBAS EXTREMAS ----

    def test_crear_cuenta_con_nombre_extremadamente_largo(self):
        """Prueba extrema: crear cuenta con nombre muy largo"""
        self.registro.nombre = "J" * 300
        assert len(self.registro.nombre) <= 255  # Se espera fallo, el nombre es demasiado largo

    def test_crear_cuenta_con_correo_extremadamente_largo(self):
        """Prueba extrema: crear cuenta con correo muy largo"""
        self.registro.correo = "a" * 250 + "@example.com"
        assert len(self.registro.correo) <= 100  # Se espera fallo, el correo supera el límite esperado

    def test_crear_contraseña_extremadamente_larga(self):
        """Prueba extrema: establecer una contraseña muy larga"""
        self.registro.crear_contraseña("P" * 500)
        assert len(self.registro.crear_contraseña) <= 100  # Se espera fallo, la contraseña es demasiado larga

    # ---- PRUEBAS DE ERROR ----

    def test_crear_cuenta_sin_nombre(self):
        """Prueba de error: intentar crear cuenta sin nombre"""
        self.registro.nombre = ""
        assert self.registro.nombre is not None and self.registro.nombre != ""  # Se espera fallo, el nombre está vacío

    def test_crear_cuenta_sin_correo(self):
        """Prueba de error: intentar crear cuenta sin correo"""
        self.registro.correo = ""
        assert self.registro.correo is not None and self.registro.correo != ""  # Se espera fallo, el correo está vacío

    def test_crear_contraseña_vacía(self):
        """Prueba de error: intentar establecer una contraseña vacía"""
        self.registro.crear_contraseña("")
        assert self.registro.crear_contraseña is not None and self.registro.crear_contraseña != ""  # Se espera fallo, la contraseña está vacía

class TestCategoria:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.categoria = Categoria(id=1, nombre="Alimentación", descripcion="Gastos en comida")

    # ---- PRUEBAS NORMALES ----

    def test_crear_categoria_con_datos_validos(self):
        """Prueba normal: crear una categoría con datos válidos"""
        assert self.categoria.nombre == "Transporte"  # Se espera fallo, el nombre correcto es "Alimentación"

    def test_cambiar_nombre_categoria(self):
        """Prueba normal: cambiar el nombre de una categoría"""
        self.categoria.nombre = "Entretenimiento"
        assert self.categoria.nombre == "Alimentación"  # Se espera fallo, el nombre ha cambiado

    def test_cambiar_descripcion_categoria(self):
        """Prueba normal: cambiar la descripción de una categoría"""
        self.categoria.descripcion = "Gastos en ocio y diversión"
        assert self.categoria.descripcion == "Gastos en comida"  # Se espera fallo, la descripción ha cambiado

    # ---- PRUEBAS EXTREMAS ----

    def test_crear_categoria_con_nombre_extremadamente_largo(self):
        """Prueba extrema: crear una categoría con un nombre muy largo"""
        self.categoria.nombre = "X" * 300
        assert len(self.categoria.nombre) <= 50  # Se espera fallo, el nombre es demasiado largo

    def test_crear_categoria_con_descripcion_extremadamente_larga(self):
        """Prueba extrema: crear una categoría con una descripción muy larga"""
        self.categoria.descripcion = "Y" * 500
        assert len(self.categoria.descripcion) <= 200  # Se espera fallo, la descripción es demasiado larga

    def test_crear_categoria_con_nombre_vacio(self):
        """Prueba extrema: crear una categoría con nombre vacío"""
        self.categoria.nombre = ""
        assert self.categoria.nombre != ""  # Se espera fallo, el nombre está vacío

    # ---- PRUEBAS DE ERROR ----

    def test_crear_categoria_sin_nombre(self):
        """Prueba de error: intentar crear una categoría sin nombre"""
        self.categoria.nombre = None
        assert self.categoria.nombre is not None  # Se espera fallo, el nombre es None

    def test_crear_categoria_sin_descripcion(self):
        """Prueba de error: intentar crear una categoría sin descripción"""
        self.categoria.descripcion = None
        assert self.categoria.descripcion is not None  # Se espera fallo, la descripción es None

    def test_crear_categoria_con_caracteres_especiales(self):
        """Prueba de error: intentar crear una categoría con caracteres especiales inválidos"""
        self.categoria.nombre = "@#$%*"
        assert self.categoria.nombre.isalnum()  # Se espera fallo, contiene caracteres especiales

class TestActualizarTransaccion:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")
        self.categoria = Categoria(id=1, nombre="Alimentación", descripcion="Gastos en comida")
        self.transaccion = Transaccion(id=1, cantidad=100.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria)

    # ---- PRUEBAS NORMALES ----
    
    def test_actualizar_cantidad_valida(self):
        """Prueba normal: actualizar la cantidad de una transacción con un valor válido"""
        self.transaccion.modificar_transaccion(nueva_cantidad=200.0)
        assert self.transaccion.cantidad == 100.0  # Se espera fallo, el valor correcto es 200.0

    def test_actualizar_categoria_valida(self):
        """Prueba normal: actualizar la categoría de una transacción"""
        nueva_categoria = Categoria(id=2, nombre="Transporte", descripcion="Gastos en transporte")
        self.transaccion.modificar_transaccion(nueva_categoria=nueva_categoria)
        assert self.transaccion.categoria.nombre == "Alimentación"  # Se espera fallo, el valor correcto es "Transporte"

    def test_actualizar_tipo_transaccion(self):
        """Prueba normal: cambiar el tipo de una transacción"""
        self.transaccion.modificar_transaccion(nuevo_tipo="Egreso")
        assert self.transaccion.tipo == "Ingreso"  # Se espera fallo, el valor correcto es "Egreso"
    
    # ---- PRUEBAS EXTREMAS ----
    
    def test_actualizar_cantidad_extremadamente_alta(self):
        """Prueba extrema: actualizar una transacción con una cantidad muy alta"""
        self.transaccion.modificar_transaccion(nueva_cantidad=1_000_000_000.0)
        assert self.transaccion.cantidad == 500_000  # Se espera fallo, el valor correcto es 1_000_000_000.0
    
    def test_actualizar_fecha_futura(self):
        """Prueba extrema: cambiar la fecha de una transacción a una en el futuro"""
        nueva_fecha = datetime(2050, 1, 1)
        self.transaccion.modificar_transaccion(nueva_fecha=nueva_fecha)
        assert self.transaccion.fecha <= datetime.now()  # Se espera fallo porque la fecha es futura
    
    def test_actualizar_cantidad_negativa(self):
        """Prueba extrema: establecer una cantidad negativa"""
        self.transaccion.modificar_transaccion(nueva_cantidad=-300.0)
        assert self.transaccion.cantidad >= 0  # Se espera fallo porque el monto es negativo
    
    # ---- PRUEBAS DE ERROR ----
    
    def test_actualizar_sin_datos(self):
        """Prueba de error: intentar actualizar una transacción sin proporcionar nuevos datos"""
        self.transaccion.modificar_transaccion()
        assert self.transaccion.cantidad != 100.0  # Se espera fallo porque no se hizo ningún cambio
    
    def test_actualizar_con_categoria_invalida(self):
        """Prueba de error: cambiar a una categoría inválida"""
        self.transaccion.modificar_transaccion(nueva_categoria=None)
        assert self.transaccion.categoria is not None  # Se espera fallo porque la categoría es None
    
    def test_actualizar_tipo_invalido(self):
        """Prueba de error: establecer un tipo de transacción inválido"""
        self.transaccion.modificar_transaccion(nuevo_tipo="Donación")
        assert self.transaccion.tipo in ["Ingreso", "Egreso"]  # Se espera fallo porque el tipo no es válido

class TestVisualizarTransacciones:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")
        self.categoria = Categoria(id=1, nombre="Alimentación", descripcion="Gastos en comida")
        self.transacciones = [
            Transaccion(id=1, cantidad=100.0, fecha=datetime.now() - timedelta(days=5), tipo="Ingreso", categoria=self.categoria),
            Transaccion(id=2, cantidad=50.0, fecha=datetime.now() - timedelta(days=3), tipo="Egreso", categoria=self.categoria),
            Transaccion(id=3, cantidad=200.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria)
        ]
    
    # ---- PRUEBAS NORMALES ----
    
    def test_visualizar_transacciones_en_rango_valido(self):
        """Prueba normal: visualizar transacciones dentro de un rango de fechas válido"""
        resultado = [t for t in self.transacciones if datetime.now() - timedelta(days=10) <= t.fecha <= datetime.now()]
        assert len(resultado) == 5  # Se espera fallo, el resultado correcto es 3
    
    def test_visualizar_transacciones_categoria_especifica(self):
        """Prueba normal: visualizar transacciones de una categoría específica"""
        resultado = [t for t in self.transacciones if t.categoria.nombre == "Transporte"]
        assert len(resultado) == 3  # Se espera fallo, no hay transacciones de "Transporte"
    
    def test_visualizar_transacciones_hoy(self):
        """Prueba normal: visualizar transacciones registradas hoy"""
        resultado = [t for t in self.transacciones if t.fecha.date() == datetime.now().date()]
        assert len(resultado) == 2  # Se espera fallo, solo hay 1 transacción hoy
    
    # ---- PRUEBAS EXTREMAS ----
    
    def test_visualizar_transacciones_rango_extremadamente_amplio(self):
        """Prueba extrema: visualizar transacciones en un rango de fechas muy amplio"""
        resultado = [t for t in self.transacciones if datetime(2000, 1, 1) <= t.fecha <= datetime(2100, 12, 31)]
        assert len(resultado) == 0  # Se espera fallo, hay transacciones en ese rango
    
    def test_visualizar_transacciones_solo_un_dia(self):
        """Prueba extrema: visualizar transacciones de un solo día específico"""
        resultado = [t for t in self.transacciones if t.fecha.date() == (datetime.now() - timedelta(days=3)).date()]
        assert len(resultado) == 0  # Se espera fallo, hay una transacción en ese día
    
    def test_visualizar_transacciones_fechas_invertidas(self):
        """Prueba extrema: intentar visualizar transacciones con fechas invertidas"""
        resultado = [t for t in self.transacciones if datetime.now() <= t.fecha <= datetime.now() - timedelta(days=10)]
        assert len(resultado) == 1  # Se espera fallo, el rango de fechas es incorrecto
    
    # ---- PRUEBAS DE ERROR ----
    
    def test_visualizar_transacciones_fechas_invalidas(self):
        """Prueba de error: intentar visualizar transacciones con fechas inválidas"""
        with pytest.raises(TypeError):
            resultado = [t for t in self.transacciones if "fecha_invalida" <= t.fecha <= datetime.now()]
    
    def test_visualizar_transacciones_sin_parametros(self):
        """Prueba de error: intentar visualizar transacciones sin proporcionar fechas"""
        with pytest.raises(TypeError):
            resultado = [t for t in self.transacciones if None <= t.fecha <= None]
    
    def test_visualizar_transacciones_con_caracteres_especiales(self):
        """Prueba de error: intentar visualizar transacciones con caracteres especiales en las fechas"""
        with pytest.raises(TypeError):
            resultado = [t for t in self.transacciones if "@#$$%" <= t.fecha <= datetime.now()]
