import datetime
import enum
from email.policy import default

from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class Empleado(db.Model, UserMixin):
    # para cambiar el nombre de la tabla, caso contrario se llamara como el nombre de la clase
    __tablename__ = "empleados"
    # atributos
    id = db.Column(db.Integer, primary_key=True)
    ci = db.Column(db.String(10), unique=True, nullable=False)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    celular = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    contrasena_encriptada = db.Column(db.String(94), nullable=False)
    nivel = db.Column(db.Enum('E', 'A'), nullable=False, server_default="E")
    date = db.Column(db.DateTime, default=datetime.datetime.now())

    # relaciones
    solicitud = db.relationship('Solicitud')
    # otros
    inserciones_incorectar = 0

    @classmethod
    def search(cls, ci, celular, email):
        cant = db.session.query(cls).where(
            cls.ci == ci or cls.celular == celular or cls.email == email).count()
        return True if cant > 0 else False

    # method to create a new empleado
    @classmethod
    def crear_empleado(cls, ci, nombres, apellidos, celular, email, contrasena, nivel='E'):
        if cls.search(ci, celular, email):
            cls.inserciones_incorectar += 1
            return None
        empleado = cls(ci=ci, nombres=nombres, apellidos=apellidos,
                       celular=celular, email=email, contrasena=contrasena, nivel=nivel)

        db.session.add(empleado)
        db.session.commit()
        return empleado

    # function to check the password
    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_encriptada, password)

    # password property, but with the @property decorator.here more information
    # https://es.acervolima.com/decorador-de-propiedades-de-python-property/#:~:text=%40property%20decorator%20es%20un%20decorador,y%20deleter%20establecidos%20como%20par%C3%A1metros.
    @property
    def contrasena(self):
        pass

    @contrasena.setter
    def contrasena(self, value):
        self.contrasena_encriptada = generate_password_hash(value)

    # mothods to get by diferent attributes
    def get_nivel(cls):
        if cls.nivel == "E":
            return "Empleado"
        return "Administrador de almacen"

    @classmethod
    def get_by_ci(cls, ci):
        return Empleado.query.filter_by(ci=ci).first()

    @classmethod
    def get_by_email(cls, email):
        return Empleado.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, id):
        return Empleado.query.filter_by(id=id).first()

    def __str__(self):
        return f'nombre: {self.nombres}, apellido: {self.apellidos}, nivel: {self.get_nivel()}'


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    # relaciones
    id_tipo_producto = db.Column(db.Integer, db.ForeignKey(
        "tipo_productos.id"), nullable=False)
    solicitud_detalle = db.relationship("SolicitudDetalle")

    @classmethod
    def create(cls, nombre, descripcion, stock, precio, id_tipo_producto):
        producto = cls(nombre=nombre, descripcion=descripcion, stock=stock,
                       precio=precio, id_tipo_producto=id_tipo_producto)

        db.session.add(producto)
        db.session.commit()
        return producto

    def __str__(self) -> str:
        return f'nombre: {self.nombre}, descripcion: {self.descripcion}, stock: {self.stock}, precio: {self.precio}'


class TipoProducto(db.Model, UserMixin):
    __tablename__ = "tipo_productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    # relaciones
    productos = db.relationship("Producto")

    @classmethod
    def create(cls, nombre):
        tipo_producto = cls(nombre=nombre)
        db.session.add(tipo_producto)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return TipoProducto.query.filter_by(id=id).first()

    def __str__(self) -> str:
        return f'id: {self.id} nombre: {self.nombre} productos: {self.productos}'


class Solicitud(db.Model):
    __tablename__ = "solicitudes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now())

    # relaciones
    id_empleado = db.Column(db.Integer, db.ForeignKey(
        "empleados.id"), nullable=False)
    solicitud_detalle = db.relationship("SolicitudDetalle")
    salida = db.relationship("Salida")

    @classmethod
    def create(cls, titulo, id_empleado):
        solicitud = Solicitud(titulo=titulo, id_empleado=id_empleado)
        db.session.add(solicitud)
        db.session.commit()
        return solicitud.id

    @classmethod
    def get_by_id(cls, id):
        return Solicitud.query.filter_by(id=id).first()

    def __str__(self) -> str:
        return f'id: {self.id}, fecha: {self.fecha}, empleado: {self.id_empleado}'


class SolicitudDetalle(db.Model):
    __tablename__ = "solicitud_detalles"

    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.Enum('A', 'P', 'R', 'D'),
                       nullable=False, server_default="P")
    # relaciones
    id_solicitud = db.Column(db.Integer, db.ForeignKey(
        "solicitudes.id"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey(
        "productos.id"), nullable=False)
    salida = db.relationship("Salida")
    #ingresos = db.relationship("Ingreso")

    def __str__(self) -> str:
        return f'id: {self.id} cantidad: {self.cantidad}, \
        observaciones: {self.observaciones}, id_solicitud: {self.id_solicitud},\
        id_producto: {self.id_producto}, estado: {self.estado}'

    @classmethod
    def create(cls, cantidad, observaciones, estado, id_solicitud, id_producto):
        solicitudD = SolicitudDetalle(cantidad=cantidad,
                                      observaciones=observaciones, estado=estado, id_solicitud=id_solicitud,
                                      id_producto=id_producto)
        db.session.add(solicitudD)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return SolicitudDetalle.query.filter_by(id=id).first()

    @classmethod
    def aceptar_solicitud(cls, id):
        solicitud = cls.get_by_id(id)
        solicitud.estado = "A"
        db.session.commit()

    @classmethod
    def rechazar_solicitud(cls, id):
        solicitud = cls.get_by_id(id)
        solicitud.estado = "R"
        db.session.commit()

    @classmethod
    def ingresar_solicitud(cls, id):
        solicitud = cls.get_by_id(id)
        solicitud.estado = "D"
        db.session.commit()

    @classmethod
    def despachar_solicitud(cls, id):
        solicitud = cls.get_by_id(id)
        solicitud.estado = "D"
        db.session.commit()

    def __str__(self) -> str:
        return f'id: {self.id} cantidad: {self.cantidad}, observaciones: {self.observaciones}, id_solicitud: {self.id_solicitud}, id_producto: {self.id_producto}'


class Ingreso(db.Model):
    __tablename__ = "ingresos"

    id = db.Column(db.Integer, primary_key=True)

    producto = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_total = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    estado = db.Column(db.Enum('D', 'P'), nullable=False, server_default="P")
    fecha = db.Column(db.DateTime, default=datetime.datetime.now())

    @classmethod
    def get_by_id(cls, id):
        return Ingreso.query.filter_by(id=id).first()

    @classmethod
    def crear_ingresos(cls, producto, cantidad, descripcion, precio_unitario, precio_total):
        ingreso = Ingreso(producto=producto, cantidad=cantidad, descripcion=descripcion,
                          precio_unitario=precio_unitario, precio_total=precio_total)

        db.session.add(ingreso)
        db.session.commit()
        return ingreso


class Salida(db.Model):
    __tablename__ = "salidas"

    id = db.Column(db.Integer, primary_key=True)
    nombre_despachante = db.Column(db.String(50), nullable=False)
    ci = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.now())

    # relaciones
    id_solicitud = db.Column(db.Integer, db.ForeignKey(
        "solicitudes.id"), nullable=False)
    id_solicitudD = db.Column(db.Integer, db.ForeignKey(
        "solicitud_detalles.id"), default=1)

    @classmethod
    def create(cls, nombre_despachante, ci, id_solicitud):
        salida = Salida(nombre_despachante=nombre_despachante,
                        ci=ci, id_solicitud=id_solicitud)
        db.session.add(salida)
        db.session.commit()
        return salida

    @classmethod
    def get_by_id(cls, id):
        return Salida.query.filter_by(id=id).first()
