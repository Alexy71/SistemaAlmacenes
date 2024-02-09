from datetime import datetime
import unittest

from flask import current_app
from app.seeds import seed_all
from app import create_app
from app import db, Empleado, Producto, TipoProducto, Solicitud, SolicitudDetalle, Ingreso, Salida
from config import configuraciones
import ddt


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        config_class = configuraciones['test']
        cls.app = create_app(config_class)
        cls.app_context = cls.app.app_context()

        seed_all()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()


@ddt.ddt
class EmpleadoTestcase(BaseTest):
    def test_login_false_empleado(self):
        empleado1 = Empleado.get_by_id(150)
        self.assertEqual(empleado1, None, 'El empleado existe')

    def test_len_cis(self):
        empleados = db.session.query(Empleado).all()
        for empleado in empleados:
            self.assertGreaterEqual(len(empleado.ci), 6)

    def test_len_names(self):
        empleados = db.session.query(Empleado).all()
        for empleado in empleados:
            self.assertRegex(empleado.nombres, '[A-Za-z]')
            self.assertGreater(len(empleado.nombres), 3)

    def test_len_surnames(self):
        empleados = db.session.query(Empleado).all()
        for empleado in empleados:
            self.assertGreaterEqual(len(empleado.apellidos), 4)

    def test_validate_emails(self):
        empleados = db.session.query(Empleado).all()
        for empleado in empleados:
            self.assertGreater(len(empleado.email), 6)
            self.assertRegex(empleado.email, '@')
            self.assertRegex(empleado.email, '.',
                             'lo sentimos, no todos son .com')

    def test_len_phone(self):
        empleados = db.session.query(Empleado).all()
        for empleado in empleados:
            self.assertGreater(len(empleado.celular), 6)

    @ddt.data(
        ('9021156', 'Martin', 'Acebey', '66620046',
         'matin@gmail.com', '123456', 'E'),
        ('9021100', 'Martin', 'Acebey', '64620040', 'mtin@gmail.com', '123456', 'E'),
        ('9021111', 'Martin', 'Acebey', '64620041',
         'martnsa@gmail.com', '123456', 'E'),
        ('9021112', 'Martin', 'Acebey', '67630041',
         'martnas@gmail.com', '123456', 'E'),
        ('9021113', 'Martin', 'Acebey', '67620041',
         'marnas@gmail.com', '123456', 'E'),
        ('9021114', 'Martin', 'Acebey', '67610041',
         'martnd@gmail.com', '123456', 'E'),
        ('9021115', 'Martin', 'Acebey', '67620441',
         'martasn@gmail.com', '123456', 'E'),
        ('9021311', 'Martin', 'Acebey', '67620341',
         'madsrtn@gmail.com', '123456', 'E'),
        ('9021411', 'Martin', 'Acebey', '67620431',
         'mastn@gmail.com', '123456', 'E'),
        ('9021011', 'Martin', 'Acebey', '67620141',
         'mdrtn@gmail.com', '123456', 'E'),
        ('9021711', 'Martin', 'Acebey', '67620241', 'matn@gmail.com', '123456', 'E'),
        ('9021211', 'Martin', 'Acebey', '67620641', 'mrtn@gmail.com', '123456', 'E'),
    )
    @ddt.unpack
    def test_a_registro(self, ci, nombres, apellidos, celular, email, contrasena, nivel):
        login = Empleado.crear_empleado(
            ci, nombres, apellidos, celular, email, contrasena, nivel)
        self.assertTrue(login.ci == ci)
        self.assertIsNotNone(login)

    @ddt.data(
        ('9021156',),
        ('9021100',),
        ('9021111',),
        ('9021112',),
        ('9021113',),
        ('9021114',),
        ('9021115',),
        ('9021311',),
        ('9021411',),
        ('9021011',),
        ('9021711',),
        ('9021211',),
    )
    @ddt.unpack
    def test_exist_empleado(self, ci):
        empleado = Empleado.get_by_ci(ci)
        self.assertIsNotNone(empleado)
        self.assertEqual(empleado.ci, ci)

    @ddt.data(
        ('9021156', '66620046', 'matin@gmail.com'),
        ('9021100', '64620040', 'mtin@gmail.com'),
        ('9021111', '64620041', 'martnsa@gmail.com'),
        ('9021112', '67630041', 'martnas@gmail.com'),
        ('9021113', '67620041', 'marnas@gmail.com'),
        ('9021114', '67610041', 'martnd@gmail.com'),
        ('9021115', '67620441', 'martasn@gmail.com'),
        ('9021311', '67620341', 'madsrtn@gmail.com'),
        ('9021411', '67620431', 'mastn@gmail.com'),
        ('9021011', '67620141', 'mdrtn@gmail.com'),
        ('9021711', '67620241', 'matn@gmail.com'),
        ('9021211', '67620641', 'mrtn@gmail.com'),
    )
    @ddt.unpack
    def test_registro(self, ci, celular, email):
        login = Empleado.search(ci, celular, email)
        self.assertIsNotNone(login)
        self.assertTrue(login)


class ProductoTestcase(BaseTest):
    def test_product_false(self):
        empleado1 = Empleado.get_by_id(15)
        self.assertEqual(empleado1, None, 'El producto no existe')
        self.assertIsNone(empleado1)

    def test_len_names(self):
        productos = db.session.query(Producto).all()
        for producto in productos:
            self.assertRegex(producto.nombre, '[A-Za-z]')
            self.assertGreater(len(producto.nombre), 3)

    def test_len_descripcion(self):
        productos = db.session.query(Producto).all()
        for producto in productos:
            self.assertRegex(producto.descripcion, '[A-Za-z]')
            self.assertGreater(len(producto.descripcion), 10)

    def test_stock(self):
        productos = db.session.query(Producto).all()
        for producto in productos:
            self.assertGreater(producto.stock, 5)
            self.assertLess(producto.stock, 1001)

    def test_precio(self):
        productos = db.session.query(Producto).all()
        for producto in productos:
            self.assertGreater(producto.precio, 0)
            self.assertLess(producto.precio, 10001)

    def test_ids_tp(self):
        productos = db.session.query(Producto).all()
        tipo_productos = db.session.query(TipoProducto).all()
        lst1, lst2 = [], []
        for i in productos:
            lst1.append(i.id_tipo_producto)

        for i in tipo_productos:
            lst2.append(i.id)

        lst1.sort()
        lst2.sort()
        lst1 = list(set(lst1))
        self.assertFalse(lst2 in lst1)


class TipoProductoTestcase(BaseTest):
    def test_tipo_product_false(self):
        empleado1 = Empleado.get_by_id(15)
        self.assertEqual(empleado1, None, 'El tipo de producto no existe')
        self.assertIsNone(empleado1)

    def test_len_names(self):
        tipo_productos = db.session.query(TipoProducto).all()
        for tipo_producto in tipo_productos:
            self.assertRegex(tipo_producto.nombre, '[A-Za-z]')
            self.assertGreaterEqual(len(tipo_producto.nombre), 2)


class SolicitudTestcase(BaseTest):
    def test_solicitud_false(self):
        solicitud = Solicitud.get_by_id(150)
        self.assertEqual(solicitud, None, 'El tipo de producto no existe')
        self.assertIsNone(solicitud)

    def test_titulo(self):
        solicitudes = db.session.query(Solicitud).all()
        for solicitud in solicitudes:
            self.assertIsNotNone(solicitud.titulo)
            self.assertRegex(solicitud.titulo, '[A-Za-z]')
            self.assertGreaterEqual(len(solicitud.titulo), 10)

    def test_fecha(self):
        solicitudes = db.session.query(Solicitud).all()
        for solicitud in solicitudes:
            self.assertIsNotNone(solicitud.fecha)
            self.assertGreaterEqual(len(solicitud.titulo), 5)
            self.assertNotEqual(solicitud.fecha, datetime.now())
            self.assertEqual(solicitud.fecha.year, datetime.now().year)

    def test_ids_tp(self):
        empleados = db.session.query(Empleado).all()
        solicitudes = db.session.query(Solicitud).all()
        lst1, lst2 = [], []
        for i in empleados:
            lst1.append(i.id)

        for i in solicitudes:
            lst2.append(i.id_empleado)

        lst1.sort()
        lst2.sort()
        lst1 = list(set(lst1))
        self.assertFalse(lst2 in lst1)


class SolicitudDetalleTestcase(BaseTest):
    def test_tipo_product_false(self):
        solicitud_detalles = SolicitudDetalle.get_by_id(150)
        self.assertEqual(solicitud_detalles, None)
        self.assertIsNone(solicitud_detalles)

    def test_observaciones(self):
        solicitud_detalles = db.session.query(SolicitudDetalle).all()
        for solicitud in solicitud_detalles:
            self.assertIsNotNone(solicitud.observaciones)
            self.assertRegex(solicitud.observaciones, '[A-Za-z]')
            self.assertGreaterEqual(len(solicitud.observaciones), 10)

    def test_cantidad(self):
        solicitud_detalles = db.session.query(SolicitudDetalle).all()
        for solicitud in solicitud_detalles:
            self.assertIsNotNone(solicitud.cantidad)
            self.assertGreater(solicitud.cantidad, 0)
            self.assertLess(solicitud.cantidad, 10000)

    def test_estado(self):
        solicitud_detalles = db.session.query(SolicitudDetalle).all()
        estados = ['A', 'P', 'R', 'D']
        for solicitud in solicitud_detalles:
            self.assertIn(solicitud.estado, estados)
            self.assertIsNotNone(solicitud.estado)

    def test_id_solicitud(self):
        solicitud_detalles = db.session.query(SolicitudDetalle).all()
        solicitudes = db.session.query(Solicitud).all()
        lst1, lst2 = [], []
        for i in solicitud_detalles:
            lst1.append(i.id)

        for i in solicitudes:
            lst2.append(i.id)

        lst1.sort()
        lst2.sort()
        lst1 = list(set(lst1))
        self.assertFalse(lst2 in lst1)

    def test_id_producto(self):
        solicitud_detalles = db.session.query(SolicitudDetalle).all()
        productos = db.session.query(Producto).all()
        lst1, lst2 = [], []
        for i in solicitud_detalles:
            lst1.append(i.id)

        for i in productos:
            lst2.append(i.id)

        lst1.sort()
        lst2.sort()
        lst1 = list(set(lst1))
        self.assertFalse(lst2 in lst1)


class SalidaTestcase(BaseTest):
    def test_tipo_product_false(self):
        salidas = Salida.get_by_id(150)
        self.assertEqual(salidas, None)
        self.assertIsNone(salidas)

    def test_nombre_despachante(self):
        salidas = db.session.query(Salida).all()
        for salida in salidas:
            self.assertIsNotNone(salida.nombre_despachante)
            self.assertRegex(salida.nombre_despachante, '[A-Za-z]')
            self.assertGreaterEqual(len(salida.nombre_despachante), 5)

    def test_ci(self):
        salidas = db.session.query(Salida).all()
        for i in salidas:
            self.assertGreater(len(i.ci), 6)

    def test_fecha(self):
        salidas = db.session.query(Salida).all()
        for solicitud in salidas:
            self.assertIsNotNone(solicitud.fecha)
            self.assertGreaterEqual(len(solicitud.titulo), 5)
            self.assertNotEqual(solicitud.fecha, datetime.now())
            self.assertEqual(solicitud.fecha.year, datetime.now().year)

    def test_id_solicitud(self):
        salidas = db.session.query(Salida).all()
        solicitudes = db.session.query(Solicitud).all()
        lst1, lst2 = [], []
        for i in salidas:
            lst1.append(i.id)

        for i in solicitudes:
            lst2.append(i.id)

        lst1.sort()
        lst2.sort()
        lst1 = list(set(lst1))
        self.assertFalse(lst2 in lst1)


class IngresosTestcase(BaseTest):
    def test_tipo_product_false(self):
        salidas = Salida.get_by_id(150)
        self.assertEqual(salidas, None)
        self.assertIsNone(salidas)

    def test_nombre_despachante(self):
        salidas = db.session.query(Salida).all()
        for salida in salidas:
            self.assertIsNotNone(salida.nombre_despachante)
            self.assertRegex(salida.nombre_despachante, '[A-Za-z]')
            self.assertGreaterEqual(len(salida.nombre_despachante), 5)

    def test_ci(self):
        salidas = db.session.query(Salida).all()
        for i in salidas:
            self.assertGreater(len(i.ci), 6)

    def test_fecha(self):
        salidas = db.session.query(Salida).all()
        for solicitud in salidas:
            self.assertIsNotNone(solicitud.fecha)
            self.assertGreaterEqual(len(solicitud.titulo), 5)
            self.assertNotEqual(solicitud.fecha, datetime.now())
            self.assertEqual(solicitud.fecha.year, datetime.now().year)

    def test_id_solicitud(self):
        salidas = db.session.query(Salida).all()
        solicitudes = db.session.query(Solicitud).all()
        lst1, lst2 = [], []
        for i in salidas:
            lst1.append(i.id)

        for i in solicitudes:
            lst2.append(i.id)

        lst1.sort()
        lst2.sort()
        lst1 = list(set(lst1))
        self.assertFalse(lst2 in lst1)
