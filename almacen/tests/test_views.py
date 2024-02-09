import unittest
from datetime import datetime
from flask import current_app
from app.seeds import seed_all
from app import create_app, db, Empleado, Producto, TipoProducto, Solicitud, SolicitudDetalle, Ingreso, Salida
from config import configuraciones
import ddt


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        config_class = configuraciones['test']
        cls.app = create_app(config_class)
        cls.app_context = cls.app.app_context()
        cls.client = cls.app.test_client()

        seed_all()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        # db.session.remove()
        # db.drop_all()
        cls.app_context.pop()

    def login(self, email, contrasena):
        return self.client.post('/', data=dict(
            email=email,
            contrasena=contrasena
        ), follow_redirects=True
        )


class AdminTestCase(BaseTest):
    def test_raiz_with_no_content(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertNotIn(b'No hay entradas', res.data)

    def test_index_with_no_content(self):
        res = self.client.get('/index')
        self.assertEqual(302, res.status_code)
        self.assertNotIn(b'No hay entradas', res.data)

    def test_y_authorized_access_a(self):
        a = self.login('kristinpowell@example.org', 'admin')
        res = self.client.get('/index')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Despacho', res.data)

        res = self.client.get('/')
        self.assertEqual(302, res.status_code)

    def test_z_authorized_access_a(self):
        res = self.client.get('/')
        self.assertEqual(302, res.status_code)
        self.assertNotIn(b'Despacho', res.data)
