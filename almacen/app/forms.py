from email.policy import default
from random import choices

from flask_wtf import FlaskForm as Form
from sqlalchemy import DateTime
from wtforms import (DateField, HiddenField, IntegerField, PasswordField,
                     RadioField, SelectField, StringField, validators)
from wtforms.fields import EmailField

from .models import Empleado, Ingreso, Producto, TipoProducto


#obligado que los atributos sea el formulario y el campo a validar
def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo los humanos pueden completar el registro!')

class RegisterForm(Form):
    honeypot = HiddenField("", validators=[ length_honeypot] )
    nombres = StringField("Nombres",validators=[
        validators.length(min=4, max=20),
    ])

    apellidos = StringField("Apellidos",validators=[
        validators.length(min=4, max=20),
    ])
    ci = IntegerField("Ci")

    nivel=SelectField("Nivel",choices=[("E","Empleado"),("A","Administrador de almacen")])

    celular = IntegerField("Celular")

    email = EmailField("Email",validators=[
        validators.length(min=4, max=50),
        validators.DataRequired(message="email requerido"),
        validators.Email(message="de un email valido")
    ])

    contrasena = PasswordField("Contrasena",validators=[
        validators.DataRequired(message="contrasena requerido"),
        validators.EqualTo("confirm_contrasena", message="no coinciden")
    ])

    confirm_contrasena = PasswordField("confirmar contrasena")

class LoginForm(Form):
    honeypot = HiddenField("")
    email = EmailField("Email",validators=[
        validators.DataRequired(message="email requerido"),
        validators.Email(message="de un email valido")
    ])

    contrasena = PasswordField("Contrasena",validators=[
        validators.DataRequired(message="contrasena requerido")
    ])


class SearchForm(Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        all = []
        tipo_producto = TipoProducto.query.order_by(TipoProducto.id.asc()).all()
        for i in tipo_producto:
            tp = (i.id, i.nombre)
            all.append(tp)
        all.append(("0", "Todos"))
        self.categoria.choices = all
        
    categoria = RadioField("Articulos: ", default="0")
    searched = StringField("Buscar")

class DespachoSearchForm(Form):
    honeypot = HiddenField("", validators=[length_honeypot] )
    nombre_despachante = StringField("Nombre", validators=[
        validators.DataRequired(message="nombre requerido"),
    ])
    ci_despachante = IntegerField("Ci", validators=[
        validators.DataRequired(message="ci requerido"),
    ])

class EntradasSalidasForm(Form):
    honeypot = HiddenField("", validators=[length_honeypot] )
    diario = RadioField("Tipo", choices=[(0,"hoy"),(1,"Manual")], default=0 )
    fecha_inicio = DateField("Fecha inicio",format='%Y-%m-%dT')
    fecha_fin = DateField("Fecha fin", format='%m/%d/%y')

class entrada(Form):
    honeypot = HiddenField("", validators=[length_honeypot] )
    producto = StringField("Producto")
    cantidad = StringField("Cantidad")
    descripcion = StringField("Descripcion")
    precio_unitario = StringField("Precio_unitario")
    precio_total = StringField("Precio_Total")


class solicitudForm(Form):
    honeypot = HiddenField("", validators=[length_honeypot] )
    titulo = StringField("Titulo")
    cantidad = IntegerField("Cantidad")
    observaciones = StringField("Observaciones")
    nombre_producto = StringField("Nombre de producto")
    precio = IntegerField("Precio")
    nombre_tipo_producto = StringField("Nombre de tipo de producto")
