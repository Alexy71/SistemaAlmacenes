from faker import Faker
from .models import *
from faker.providers import BaseProvider
from faker.generator import random
fake = Faker()
Faker.seed(12)

EMPLEADOS = 10
SOLICITUDES = 10
TIPOPRODUCTO = 10


def get_ids(cls):
    ids = []
    for i in db.session.query(cls.id).order_by(cls.id.desc()).all():
        ids.append(i[0])
    return ids


class MyProvider(BaseProvider):
    def empleado_password(self, type):
        if type == 'E':
            return '123456'
        return 'admin'


fake.add_provider(MyProvider)


def seed_empleado():
    for _ in range(EMPLEADOS):
        ci = fake.unique.random_int(min=1000000, max=9999999)
        nombres = fake.first_name()
        apellidos = fake.last_name()
        celular = fake.unique.phone_number()
        email = fake.unique.email()
        nivel = random.choice(['E', 'A'])
        contrasena = fake.empleado_password(nivel)
        Empleado.crear_empleado(ci, nombres, apellidos,
                                celular, email, contrasena, nivel)


def seed_solicitud():
    for _ in range(SOLICITUDES):
        titulo = fake.sentence()
        id_empleado = random.choice(get_ids(Empleado))
        Solicitud.create(titulo, id_empleado)


def seed_solicitudD():
    ids_solicitudes = get_ids(Solicitud)
    ids_productos = get_ids(Producto)
    for _ in range(SOLICITUDES//2):
        cantidad = fake.random_int(min=1, max=1000)
        observaciones = fake.sentence()
        estado = random.choice(['A', 'P', 'R', 'D'])
        id_solicitud = random.choice(ids_solicitudes)
        id_producto = random.choice(ids_productos)

        SolicitudDetalle.create(cantidad, observaciones,
                                estado, id_solicitud, id_producto)


def seed_tipo_product():
    for _ in range(TIPOPRODUCTO):
        nombre = fake.unique.word()
        TipoProducto.create(nombre)


def seed_producto():
    for _ in range(TIPOPRODUCTO*2):
        nombre = fake.unique.word() + ' ' + fake.word()
        descripcion = fake.sentence()
        stock = fake.random_int(min=1, max=1000)
        precio = fake.random_int(min=1, max=10000)
        id_tipo_producto = random.choice(get_ids(TipoProducto))
        Producto.create(nombre, descripcion, stock, precio, id_tipo_producto)


def seed_all():
    seed_empleado()
    seed_solicitud()
    seed_tipo_product()
    seed_producto()
    seed_solicitudD()
