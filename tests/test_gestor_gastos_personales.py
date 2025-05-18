import pytest
from src.model.transaccion import Transaccion
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from src.model.base import Base  # Importa Base desde base.py
from sqlalchemy.orm import sessionmaker
from src.model.usuario import Usuario
from src.model.categoria import Categoria, TipoCategoria
from src.model.registros import Registro
from src.model.errors import CorreoInvalidoError, ContrasenaInseguraError, CamposVaciosError, FechaFuturaError, CantidadNegativaError, UsuarioNoEncontradoError, CategoriaInvalidaError, TipoTransaccionInvalidoError, ContrasenaIncorrectaError
from datetime import datetime, timedelta
from src.model.errors import (
    CantidadNegativaError,
    TipoTransaccionInvalidoError,
    CategoriaInvalidaError,
    FechaFuturaError
)

class TestTransaccion:
    def setup_method(self):
        """Configuración antes de cada prueba"""
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(bind=engine)
        TestingSessionLocal = sessionmaker(bind=engine)
        self.session = TestingSessionLocal()

        self.usuario = Usuario(nombre="Juan", correo="juan@example.com", contraseña="segura123")
        self.categoria = Categoria(
            nombre="Alimentación",
            tipo="Egreso",  # Aseguramos que el tipo esté capitalizado
            descripcion="Gastos relacionados con comida"
        )

        self.session.add_all([self.usuario, self.categoria])
        self.session.commit()

    def teardown_method(self):
        self.session.close()

    def test_registrar_transaccion_con_datos_validos(self):
        transaccion = Transaccion(
            cantidad=100.0,
            fecha=datetime.now(),
            tipo="Egreso",
            categoria=self.categoria,
            usuario=self.usuario,
            session=self.session
        )
        self.session.add(transaccion)
        self.session.commit()

        t_db = self.session.query(Transaccion).filter_by(id=transaccion.id).first()
        assert t_db is not None
        assert t_db.cantidad == 100.0

    def test_actualizar_transaccion_existente(self):
        transaccion = Transaccion(
            cantidad=200.0,
            fecha=datetime.now(),
            tipo="Egreso",
            categoria=self.categoria,
            usuario=self.usuario,
            session=self.session
        )
        self.session.add(transaccion)
        self.session.commit()

        transaccion.modificar_cantidad(250.0)
        self.session.commit()

        t_db = self.session.query(Transaccion).filter_by(id=transaccion.id).first()
        assert t_db.cantidad == 250.0

    def test_visualizar_transacciones_por_categoria(self):
        t1 = Transaccion(50.0, datetime.now(), "Egreso", self.categoria, self.usuario, self.session)
        t2 = Transaccion(75.0, datetime.now(), "Egreso", self.categoria, self.usuario, self.session)
        self.session.add_all([t1, t2])
        self.session.commit()

        transacciones = self.session.query(Transaccion).filter_by(categoria_id=self.categoria.id).all()
        assert len(transacciones) == 2

    def test_registrar_transaccion_con_monto_extremadamente_alto(self):
        transaccion = Transaccion(
            cantidad=1_000_000_000.0,
            fecha=datetime.now(),
            tipo="Egreso",
            categoria=self.categoria,
            usuario=self.usuario,
            session=self.session
        )
        self.session.add(transaccion)
        self.session.commit()
        assert transaccion.cantidad == 1_000_000_000.0

    def test_registrar_transaccion_con_fecha_futura(self):
        with pytest.raises(ValueError, match="La fecha no puede ser futura"):
            Transaccion(
                cantidad=200.0,
                fecha=datetime.now() + timedelta(days=365),
                tipo="Egreso",
                categoria=self.categoria,
                usuario=self.usuario,
                session=self.session
            )

    def test_registrar_transaccion_con_monto_negativo(self):
        with pytest.raises(ValueError, match="El monto de la transacción no puede ser negativo"):
            Transaccion(
                cantidad=-500.0,
                fecha=datetime.now(),
                tipo="Egreso",
                categoria=self.categoria,
                usuario=self.usuario,
                session=self.session
            )

    def test_registrar_transaccion_sin_usuario(self):
        with pytest.raises(ValueError, match="Usuario no válido"):
            Transaccion(
                cantidad=100.0,
                fecha=datetime.now(),
                tipo="Egreso",
                categoria=self.categoria,
                usuario=None,
                session=self.session
            )

    def test_registrar_transaccion_sin_categoria(self):
        with pytest.raises(ValueError):
            Transaccion(
                cantidad=50.0,
                fecha=datetime.now(),
                tipo="Egreso",
                categoria=None,
                usuario=self.usuario,
                session=self.session
            )

    def test_registrar_transaccion_con_tipo_invalido(self):
        with pytest.raises(ValueError, match="Tipo debe ser 'Ingreso' o 'Egreso'"):
            Transaccion(
                cantidad=300.0,
                fecha=datetime.now(),
                tipo="Donación",
                categoria=self.categoria,
                usuario=self.usuario,
                session=self.session
            )

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
        self.registro = Registro(
            id=1,
            nombre="Juan",
            correo="juan@example.com",
            contrasena="segura123"  # contraseña válida para pasar la validación
        )

    
    # ---- PRUEBAS NORMALES ----

    def test_crear_cuenta_con_datos_validos(self):
        """Prueba normal: crear una cuenta con datos válidos"""
        assert self.registro.nombre == "Juan"  # El nombre correcto es "Juan"

    def test_crear_cuenta_con_correo_valido(self):
        """Prueba normal: registrar cuenta con correo válido"""
        assert self.registro.correo == "juan@example.com"  # El correo correcto es "juan@example.com"

    def test_crear_contraseña_correctamente(self):
        """Prueba normal: establecer una contraseña correctamente"""
        self.registro.establecer_contrasena("NuevaClave123")
        assert self.registro.contrasena == "NuevaClave123"  # La contraseña es correcta
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
        self.registro.establecer_contrasena("P" * 500)
        assert len(self.registro.contrasena) > 100  # La contraseña es demasiado larga
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
        with pytest.raises(CamposVaciosError):
            self.registro.establecer_contrasena("")

    def test_crear_cuenta_con_correo_invalido(self):
        """Prueba de error: crear cuenta con correo inválido"""
        with pytest.raises(CorreoInvalidoError):
            self.registro.establecer_datos_personales(nombre="Pedro", correo="correo_invalido")

    def test_crear_contraseña_corta(self):
        """Prueba de error: establecer una contraseña muy corta"""
        with pytest.raises(ContrasenaInseguraError):
            self.registro.establecer_contrasena("123")


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
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        TestingSessionLocal = sessionmaker(bind=engine)
        self.session = TestingSessionLocal()

        self.usuario = Usuario(nombre="Juan", correo="juan@example.com", contraseña="segura123")
        self.session.add(self.usuario)
        self.session.commit()

        from src.model.categoria import TipoCategoria
        self.categoria = Categoria(
            nombre="Salario",
            tipo=TipoCategoria.INGRESO,
            descripcion="Pago mensual"
        )
        self.session.add(self.categoria)
        self.session.commit()

    # Recargar para asegurarse que es la misma instancia que en la DB
        self.categoria = self.session.query(Categoria).filter_by(nombre="Salario").first()

        self.transaccion = Transaccion(
            id=1,
            cantidad=100.0,
            fecha=datetime.now(),
            tipo="Ingreso",   # Aquí puede seguir siendo string, pues tu validación en Transaccion lo maneja
            categoria=self.categoria,
            usuario=self.usuario,
            session=self.session
    )



    # ---- PRUEBAS NORMALES ----

    def test_actualizar_cantidad_valida(self):
        """Prueba normal: actualizar la cantidad de una transacción con un valor válido"""
        self.transaccion.modificar_transaccion(nueva_cantidad=200.0)
        assert self.transaccion.cantidad == 200.0

    def test_actualizar_categoria_valida(self):
        """Prueba normal: actualizar la categoría de una transacción"""
        nueva_categoria = Categoria(
            id=2,
            nombre="Venta",
            tipo="Ingreso",  # Debe coincidir con el tipo de transacción
            descripcion="Ingreso por ventas"
        )
        self.session.add(nueva_categoria)
        self.session.commit()

        self.transaccion.modificar_transaccion(nueva_categoria=nueva_categoria)
        assert self.transaccion.categoria.nombre == "Venta"

    def test_actualizar_tipo_transaccion(self):
        """Prueba normal: cambiar el tipo de una transacción"""
        # Crear una categoría válida para egreso
        nueva_categoria = Categoria(
            id=3,
            nombre="Alimentación",
            tipo="Egreso",
            descripcion="Gastos de comida"
        )
        self.session.add(nueva_categoria)
        self.session.commit()

        # Cambiar tipo y categoría al mismo tiempo
        self.transaccion.modificar_transaccion(nuevo_tipo="Egreso", nueva_categoria=nueva_categoria)
        assert self.transaccion.tipo == "Egreso"
        assert self.transaccion.categoria.nombre == "Alimentación"

    # ---- PRUEBAS EXTREMAS ----

    def test_actualizar_cantidad_extremadamente_alta(self):
        """Prueba extrema: actualizar una transacción con una cantidad muy alta"""
        self.transaccion.modificar_transaccion(nueva_cantidad=1_000_000_000.0)
        assert self.transaccion.cantidad == 1_000_000_000.0

    def test_actualizar_fecha_futura(self):
        """Prueba extrema: cambiar la fecha de una transacción a una en el futuro"""
        nueva_fecha = datetime(2050, 1, 1)
        with pytest.raises(FechaFuturaError):
            self.transaccion.modificar_transaccion(nueva_fecha=nueva_fecha)

    def test_actualizar_cantidad_negativa(self):
        """Prueba extrema: establecer una cantidad negativa"""
        with pytest.raises(CantidadNegativaError):
            self.transaccion.modificar_transaccion(nueva_cantidad=-300.0)

    # ---- PRUEBAS DE ERROR ----

    def test_actualizar_sin_datos(self):
        """Prueba de error: intentar actualizar una transacción sin proporcionar nuevos datos"""
        with pytest.raises(ValueError):
            self.transaccion.modificar_transaccion()

    def test_actualizar_con_categoria_invalida(self):
        """Prueba de error: cambiar a una categoría inválida"""
        with pytest.raises(CategoriaInvalidaError):
            self.transaccion.modificar_transaccion(nueva_categoria="Categoría Inventada")

    def test_actualizar_tipo_invalido(self):
        """Prueba de error: establecer un tipo de transacción inválido"""
        with pytest.raises(TipoTransaccionInvalidoError):
            self.transaccion.modificar_transaccion(nuevo_tipo="Donación")

class TestVisualizarTransacciones:
    def setup_method(self):
        self.usuario = Usuario(id=1, nombre="Juan", correo="juan@example.com", contraseña="segura123")
        self.categoria = Categoria(id=1, nombre="Alimentación", descripcion="Gastos relacionados con comida", tipo="Ingreso")

    # Creamos el mock para session
        self.mock_session = MagicMock()

    # Mockear el query para que filtre y devuelva la categoría que queremos
        query_mock = MagicMock()
        filter_mock = MagicMock()
        filter_mock.all.return_value = [self.categoria]  # La lista que se retorna al llamar all()
        query_mock.filter.return_value = filter_mock
        self.mock_session.query.return_value = query_mock

        self.transacciones = [
            Transaccion(id=1, cantidad=100.0, fecha=datetime.now() - timedelta(days=5), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario, session=self.mock_session),
            Transaccion(id=2, cantidad=50.0, fecha=datetime.now() - timedelta(days=3), tipo="Egreso", categoria=self.categoria, usuario=self.usuario, session=self.mock_session),
            Transaccion(id=3, cantidad=200.0, fecha=datetime.now(), tipo="Ingreso", categoria=self.categoria, usuario=self.usuario, session=self.mock_session)
        ]
    
    # ---- PRUEBAS NORMALES ----
    
    def test_visualizar_transacciones_en_rango_valido(self):
        """Prueba normal: visualizar transacciones dentro de un rango de fechas válido"""
        resultado = [t for t in self.transacciones if datetime.now() - timedelta(days=10) <= t.fecha <= datetime.now()]
        assert len(resultado) == 3
    
    def test_visualizar_transacciones_categoria_especifica(self):
        """Prueba normal: visualizar transacciones de una categoría específica"""
        # Aquí comparas el nombre de la categoría
        resultado = [t for t in self.transacciones if t.categoria.nombre == "Transporte"]
        assert len(resultado) == 0
    
    def test_visualizar_transacciones_hoy(self):
        """Prueba normal: visualizar transacciones registradas hoy"""
        resultado = [t for t in self.transacciones if t.fecha.date() == datetime.now().date()]
        assert len(resultado) == 1
    
    # ---- PRUEBAS EXTREMAS ----
    
    def test_visualizar_transacciones_rango_extremadamente_amplio(self):
        """Prueba extrema: visualizar transacciones en un rango de fechas muy amplio"""
        resultado = [t for t in self.transacciones if datetime(2000, 1, 1) <= t.fecha <= datetime(2100, 12, 31)]
        assert len(resultado) == 3
    
    def test_visualizar_transacciones_solo_un_dia(self):
        """Prueba extrema: visualizar transacciones de un solo día específico"""
        resultado = [t for t in self.transacciones if t.fecha.date() == (datetime.now() - timedelta(days=3)).date()]
        assert len(resultado) == 1
    
    def test_visualizar_transacciones_fechas_invertidas(self):
        """Prueba extrema: intentar visualizar transacciones con fechas invertidas"""
        resultado = [t for t in self.transacciones if datetime.now() <= t.fecha <= datetime.now() - timedelta(days=10)]
        assert len(resultado) == 0
    
    # ---- PRUEBAS DE ERROR ----
    
    def test_visualizar_transacciones_fechas_invalidas(self):
        """Prueba de error: intentar visualizar transacciones con fechas inválidas"""
        with pytest.raises(TypeError):
            resultado = [t for t in self.transacciones if None <= t.fecha <= datetime.now()]
    
    def test_visualizar_transacciones_sin_parametros(self):
        """Prueba de error: intentar visualizar transacciones sin proporcionar fechas"""
        with pytest.raises(TypeError):
            resultado = [t for t in self.transacciones if None <= t.fecha <= None]
    
    def test_visualizar_transacciones_con_caracteres_especiales(self):
        """Prueba de error: intentar visualizar transacciones con caracteres especiales en las fechas"""
        with pytest.raises(TypeError):
            resultado = [t for t in self.transacciones if datetime(2021, 1, 1) <= t.fecha <= "fecha_invalida"]