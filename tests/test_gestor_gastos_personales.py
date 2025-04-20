import pytest
from src.model.transaccion import Transaccion
from src.model.usuario import Usuario
from src.model.categoria import Categoria
from src.model.registros import Registros
from src.model.errors import CorreoInvalidoError, ContrasenaInseguraError, CamposVaciosError, FechaFuturaError, CantidadNegativaError, UsuarioNoEncontradoError, CategoriaInvalidaError, TipoTransaccionInvalidoError, ContrasenaIncorrectaError
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
        assert transaccion.cantidad == 100.0  # Valor correcto es 100.0

    def test_actualizar_transaccion_existente(self):
        """Prueba normal: actualizar una transacción existente"""
        transaccion = Transaccion(id=2, cantidad=200.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)
        transaccion.cantidad = 300.0
        assert transaccion.cantidad == 300.0  # Valor correcto es 300.0

    def test_visualizar_transacciones_por_categoria(self):
        """Prueba normal: visualizar transacciones de una categoría"""
        transacciones = [
            Transaccion(id=3, cantidad=50.0, fecha=datetime.now(), tipo="Egreso", categoria=self.categoria, usuario=self.usuario),
            Transaccion(id=4, cantidad=75.0, fecha=datetime.now(), tipo="Egreso", categoria=self.categoria, usuario=self.usuario)
        ]
        total = sum(t.cantidad for t in transacciones)
        assert total == 125  # Total correcto es 125

    # ---- PRUEBAS EXTREMAS ----

    def test_registrar_transaccion_con_monto_extremadamente_alto(self):
        """Prueba extrema: registrar una transacción con un monto muy alto"""
        transaccion = Transaccion(id=5, cantidad=1_000_000_000.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)
        assert transaccion.cantidad == 1_000_000_000.0  # Valor correcto es 1_000_000_000.0

    def test_registrar_transaccion_con_fecha_futura(self):
        """Prueba extrema: registrar una transacción con una fecha en el futuro"""
        with pytest.raises(FechaFuturaError):
            Transaccion(id=6, cantidad=200.0, fecha=datetime.now() + timedelta(days=365), tipo="Egreso", categoria=self.categoria, usuario=self.usuario)

    def test_registrar_transaccion_con_monto_negativo(self):
        """Prueba extrema: registrar una transacción con un monto negativo"""
        with pytest.raises(CantidadNegativaError):
            Transaccion(id=7, cantidad=-500.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)

    # ---- PRUEBAS DE ERROR ----

    def test_registrar_transaccion_sin_usuario(self):
        """Prueba de error: registrar una transacción sin usuario"""
        with pytest.raises(UsuarioNoEncontradoError):
            Transaccion(id=8, cantidad=100.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=None)

    def test_registrar_transaccion_sin_categoria(self):
        """Prueba de error: registrar una transacción sin categoría"""
        with pytest.raises(CategoriaInvalidaError):
            Transaccion(id=9, cantidad=50.0, fecha=datetime.now(), tipo="Egreso", categoria=None, usuario=self.usuario)

    def test_registrar_transaccion_con_tipo_invalido(self):
        """Prueba de error: registrar una transacción con un tipo no válido"""
        with pytest.raises(TipoTransaccionInvalidoError):
            Transaccion(id=10, cantidad=300.0, fecha=datetime.now(), tipo="Donación", categoria=self.categoria, usuario=self.usuario)


class TestUsuario:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="Segura123")

    # ---- PRUEBAS NORMALES ----

    def test_crear_usuario_con_datos_validos(self):
        """Prueba normal: crear un usuario con datos válidos"""
        assert self.usuario.nombre == "Juan"  # El nombre correcto es "Juan"

    def test_iniciar_sesion_con_credenciales_correctas(self):
        """Prueba normal: iniciar sesión con credenciales correctas"""
        assert self.usuario.contraseña == "Segura123"  # La contraseña correcta es "Segura123"

    def test_cambiar_contraseña_correctamente(self):
        """Prueba normal: cambiar la contraseña correctamente"""
        self.usuario.contraseña = "NuevaClave123"
        assert self.usuario.contraseña == "NuevaClave123"  # La contraseña ha cambiado

    # ---- PRUEBAS EXTREMAS ----

    def test_crear_usuario_con_nombre_extremadamente_largo(self):
        """Prueba extrema: crear usuario con nombre muy largo"""
        self.usuario.nombre = "J" * 300
        assert len(self.usuario.nombre) > 255  # El nombre es demasiado largo

    def test_crear_usuario_con_correo_extremadamente_largo(self):
        """Prueba extrema: crear usuario con correo muy largo"""
        self.usuario.correo = "a" * 250 + "@example.com"
        assert len(self.usuario.correo) > 100  # El correo supera el límite esperado

    def test_cambiar_contraseña_a_una_extremadamente_larga(self):
        """Prueba extrema: cambiar la contraseña a una muy larga"""
        self.usuario.contraseña = "P" * 500
        assert len(self.usuario.contraseña) > 100  # La contraseña es demasiado larga

    # ---- PRUEBAS DE ERROR ----

    def test_crear_usuario_sin_nombre(self):
        """Prueba de error: crear usuario sin nombre"""
        self.usuario.nombre = ""
        with pytest.raises(CamposVaciosError):
            Usuario(id=1, nombre=self.usuario.nombre, correo=self.usuario.correo, contraseña=self.usuario.contraseña)

    def test_crear_usuario_sin_correo(self):
        """Prueba de error: crear usuario sin correo"""
        self.usuario.correo = ""
        with pytest.raises(CamposVaciosError):
            Usuario(id=1, nombre=self.usuario.nombre, correo=self.usuario.correo, contraseña=self.usuario.contraseña)

    def test_crear_usuario_sin_contraseña(self):
        """Prueba de error: crear usuario sin contraseña"""
        self.usuario.contraseña = ""
        with pytest.raises(CamposVaciosError):
            Usuario(id=1, nombre=self.usuario.nombre, correo=self.usuario.correo, contraseña=self.usuario.contraseña)

    def test_crear_usuario_con_correo_invalido(self):
        """Prueba de error: crear usuario con correo inválido"""
        with pytest.raises(CorreoInvalidoError):
            Usuario(id=2, nombre="Pedro", correo="correo_invalido", contraseña="Segura123")

    def test_crear_usuario_con_contraseña_corta(self):
        """Prueba de error: crear usuario con contraseña corta"""
        with pytest.raises(ContrasenaInseguraError):
            Usuario(id=3, nombre="Ana", correo="ana@example.com", contraseña="123")

    def test_cambiar_contraseña_corta(self):
        """Prueba de error: cambiar la contraseña a una muy corta"""
        with pytest.raises(ContrasenaInseguraError):
            self.usuario.cambiar_contraseña("123")

    def test_iniciar_sesion_con_credenciales_incorrectas(self):
        """Prueba de error: iniciar sesión con credenciales incorrectas"""
        with pytest.raises(ContrasenaIncorrectaError):
            self.usuario.iniciar_sesion("juan@example.com", "incorrecta")

class TestRegistros:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.registro = Registros(id=1, nombre="Juan", correo="juan@example.com")

    # ---- PRUEBAS NORMALES ----

    def test_crear_cuenta_con_datos_validos(self):
        """Prueba normal: crear una cuenta con datos válidos"""
        assert self.registro.nombre == "Juan"  # El nombre correcto es "Juan"

    def test_crear_cuenta_con_correo_valido(self):
        """Prueba normal: registrar cuenta con correo válido"""
        assert self.registro.correo == "juan@example.com"  # El correo correcto es "juan@example.com"

    def test_crear_contraseña_correctamente(self):
        """Prueba normal: establecer una contraseña correctamente"""
        self.registro.crear_contraseña("NuevaClave123")
        assert self.registro.contraseña == "NuevaClave123"  # La contraseña es correcta

    # ---- PRUEBAS EXTREMAS ----

    def test_crear_cuenta_con_nombre_extremadamente_largo(self):
        """Prueba extrema: crear cuenta con nombre muy largo"""
        self.registro.nombre = "J" * 300
        assert len(self.registro.nombre) > 255  # El nombre es demasiado largo

    def test_crear_cuenta_con_correo_extremadamente_largo(self):
        """Prueba extrema: crear cuenta con correo muy largo"""
        self.registro.correo = "a" * 250 + "@example.com"
        assert len(self.registro.correo) > 100  # El correo supera el límite esperado

    def test_crear_contraseña_extremadamente_larga(self):
        """Prueba extrema: establecer una contraseña muy larga"""
        self.registro.crear_contraseña("P" * 500)
        assert len(self.registro.contraseña) > 100  # La contraseña es demasiado larga

    # ---- PRUEBAS DE ERROR ----

    def test_crear_cuenta_sin_nombre(self):
        """Prueba de error: intentar crear cuenta sin nombre"""
        self.registro.nombre = ""
        assert self.registro.nombre is None or self.registro.nombre == ""  # El nombre está vacío

    def test_crear_cuenta_sin_correo(self):
        """Prueba de error: intentar crear cuenta sin correo"""
        self.registro.correo = ""
        assert self.registro.correo is None or self.registro.correo == ""  # El correo está vacío

    def test_crear_contraseña_vacía(self):
        """Prueba de error: intentar establecer una contraseña vacía"""
        self.registro.crear_contraseña("")
        assert self.registro.contraseña is None or self.registro.contraseña == ""  # La contraseña está vacía

    def test_crear_cuenta_con_correo_invalido(self):
        """Prueba de error: crear cuenta con correo inválido"""
        with pytest.raises(CorreoInvalidoError):
            self.registro.crear_cuenta(nombre="Pedro", correo="correo_invalido")

    def test_crear_contraseña_corta(self):
        """Prueba de error: establecer una contraseña muy corta"""
        with pytest.raises(ContrasenaInseguraError):
            self.registro.crear_contraseña("123")

class TestCategoria:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.categoria = Categoria(id=1, nombre="Alimentación", descripcion="Gastos en comida")

    # ---- PRUEBAS NORMALES ----

    def test_crear_categoria_con_datos_validos(self):
        """Prueba normal: crear una categoría con datos válidos"""
        assert self.categoria.nombre == "Alimentación"  # El nombre correcto es "Alimentación"

    def test_cambiar_nombre_categoria(self):
        """Prueba normal: cambiar el nombre de una categoría"""
        self.categoria.nombre = "Entretenimiento"
        assert self.categoria.nombre == "Entretenimiento"  # El nombre ha cambiado

    def test_cambiar_descripcion_categoria(self):
        """Prueba normal: cambiar la descripción de una categoría"""
        self.categoria.descripcion = "Gastos en ocio y diversión"
        assert self.categoria.descripcion == "Gastos en ocio y diversión"  # La descripción ha cambiado

    # ---- PRUEBAS EXTREMAS ----

    def test_crear_categoria_con_nombre_extremadamente_largo(self):
        """Prueba extrema: crear una categoría con un nombre muy largoo"""
        with pytest.raises(ValueError):
            Categoria(id=1, nombre="X" * 300, descripcion="Gastos en comida")

    def test_crear_categoria_con_descripcion_extremadamente_larga(self):
        """Prueba extrema: crear una categoría con una descripción muy larga"""
        self.categoria.descripcion = "Y" * 500
        assert len(self.categoria.descripcion) > 200  # La descripción es demasiado larga

    def test_crear_categoria_con_nombre_vacio(self):
        """Prueba extrema: crear una categoría con nombre vacío"""
        with pytest.raises(ValueError):
            Categoria(id=1, nombre="", descripcion="Gastos en comida")

    # ---- PRUEBAS DE ERROR ----

    def test_crear_categoria_sin_nombre(self):
        """Prueba de error: intentar crear una categoría sin nombre"""
        with pytest.raises(ValueError):
            Categoria(id=1, nombre=None, descripcion="Gastos en comida")

    def test_crear_categoria_sin_descripcion(self):
        """Prueba de error: intentar crear una categoría sin descripción"""
        self.categoria.descripcion = None
        assert self.categoria.descripcion is None  # La descripción es None

    def test_crear_categoria_con_caracteres_especiales(self):
        """Prueba de error: intentar crear una categoría con caracteres especiales inválidos"""
        with pytest.raises(ValueError):
            Categoria(id=1, nombre="@#$%*", descripcion="Gastos en comida")

class TestActualizarTransaccion:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")
        self.categoria = Categoria(id=1, nombre="Alimentación", descripcion="Gastos en comida")
        self.transaccion = Transaccion(id=1, cantidad=100.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)

    # ---- PRUEBAS NORMALES ----
    
    def test_actualizar_cantidad_valida(self):
        """Prueba normal: actualizar la cantidad de una transacción con un valor válido"""
        self.transaccion.modificar_transaccion(nueva_cantidad=200.0)
        assert self.transaccion.cantidad == 200.0  # Valor correcto es 200.0

    def test_actualizar_categoria_valida(self):
        """Prueba normal: actualizar la categoría de una transacción"""
        nueva_categoria = Categoria(id=2, nombre="Transporte", descripcion="Gastos en transporte")
        self.transaccion.modificar_transaccion(nueva_categoria=nueva_categoria)
        assert self.transaccion.categoria.nombre == "Transporte"  # Valor correcto es "Transporte"

    def test_actualizar_tipo_transaccion(self):
        """Prueba normal: cambiar el tipo de una transacción"""
        self.transaccion.modificar_transaccion(nuevo_tipo="Egreso")
        assert self.transaccion.tipo == "Egreso"  # Valor correcto es "Egreso"
    
    # ---- PRUEBAS EXTREMAS ----
    
    def test_actualizar_cantidad_extremadamente_alta(self):
        """Prueba extrema: actualizar una transacción con una cantidad muy alta"""
        self.transaccion.modificar_transaccion(nueva_cantidad=1_000_000_000.0)
        assert self.transaccion.cantidad == 1_000_000_000.0  # Valor correcto es 1_000_000_000.0
    
    def test_actualizar_fecha_futura(self):
        """Prueba extrema: cambiar la fecha de una transacción a una en el futuro"""
        nueva_fecha = datetime(2050, 1, 1)
        self.transaccion.modificar_transaccion(nueva_fecha=nueva_fecha)
        assert self.transaccion.fecha > datetime.now()  # La fecha es futura
    
    def test_actualizar_cantidad_negativa(self):
        """Prueba extrema: establecer una cantidad negativa"""
        self.transaccion.modificar_transaccion(nueva_cantidad=-300.0)
        assert self.transaccion.cantidad < 0  # El monto es negativo
    
    # ---- PRUEBAS DE ERROR ----
    
    def test_actualizar_sin_datos(self):
        """Prueba de error: intentar actualizar una transacción sin proporcionar nuevos datos"""
        self.transaccion.modificar_transaccion()
        assert self.transaccion.cantidad == 100.0  # No se hizo ningún cambio
    
    def test_actualizar_con_categoria_invalida(self):
        """Prueba de error: cambiar a una categoría inválida"""
        with pytest.raises(CategoriaInvalidaError):
            self.transaccion.modificar_transaccion(nueva_categoria=None)

    def test_actualizar_tipo_invalido(self):
        """Prueba de error: establecer un tipo de transacción inválido"""
        with pytest.raises(TipoTransaccionInvalidoError):
            self.transaccion.modificar_transaccion(nuevo_tipo="Donación")

class TestVisualizarTransacciones:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")
        self.categoria = Categoria(id=1, nombre="Alimentación", descripcion="Gastos en comida")
        self.transacciones = [
            Transaccion(id=1, cantidad=100.0, fecha=datetime.now() - timedelta(days=5), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario),
            Transaccion(id=2, cantidad=50.0, fecha=datetime.now() - timedelta(days=3), tipo="Egreso", categoria=self.categoria, usuario=self.usuario),
            Transaccion(id=3, cantidad=200.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario)
        ]
    
    # ---- PRUEBAS NORMALES ----
    
    def test_visualizar_transacciones_en_rango_valido(self):
        """Prueba normal: visualizar transacciones dentro de un rango de fechas válido"""
        resultado = [t for t in self.transacciones if datetime.now() - timedelta(days=10) <= t.fecha <= datetime.now()]
        assert len(resultado) == 3  # El resultado correcto es 3
    
    def test_visualizar_transacciones_categoria_especifica(self):
        """Prueba normal: visualizar transacciones de una categoría específica"""
        resultado = [t for t in self.transacciones if t.categoria.nombre == "Transporte"]
        assert len(resultado) == 0  # No hay transacciones de "Transporte"
    
    def test_visualizar_transacciones_hoy(self):
        """Prueba normal: visualizar transacciones registradas hoy"""
        resultado = [t for t in self.transacciones if t.fecha.date() == datetime.now().date()]
        assert len(resultado) == 1  # Solo hay 1 transacción hoy
    
    # ---- PRUEBAS EXTREMAS ----
    
    def test_visualizar_transacciones_rango_extremadamente_amplio(self):
        """Prueba extrema: visualizar transacciones en un rango de fechas muy amplio"""
        resultado = [t for t in self.transacciones if datetime(2000, 1, 1) <= t.fecha <= datetime(2100, 12, 31)]
        assert len(resultado) == 3  # Hay transacciones en ese rango
    
    def test_visualizar_transacciones_solo_un_dia(self):
        """Prueba extrema: visualizar transacciones de un solo día específico"""
        resultado = [t for t in self.transacciones if t.fecha.date() == (datetime.now() - timedelta(days=3)).date()]
        assert len(resultado) == 1  # Hay una transacción en ese día
    
    def test_visualizar_transacciones_fechas_invertidas(self):
        """Prueba extrema: intentar visualizar transacciones con fechas invertidas"""
        resultado = [t for t in self.transacciones if datetime.now() <= t.fecha <= datetime.now() - timedelta(days=10)]
        assert len(resultado) == 0  # El rango de fechas es incorrecto
    
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
