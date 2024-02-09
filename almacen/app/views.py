from flask import Blueprint, jsonify
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from app.conts import TASK_SOLICITUD_APROBADA, TASK_SOLICITUD_RECHAZADA

from .models import *
from .forms import *
from . import login_manager, db

page = Blueprint("page", __name__)


@login_manager.user_loader
def load_user(id):
    return Empleado.get_by_id(id)


@page.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        empleado = Empleado.get_by_email(form.email.data)
        if empleado and empleado.verificar_contrasena(form.contrasena.data):
            login_user(empleado)
            return redirect(url_for(".index"))
    return render_template("auth/login.html", title="Login", form=form)


@page.route("/registrarse", methods=['GET', 'POST'])
def registrarse():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        empleado = Empleado.crear_empleado(form.ci.data, form.nombres.data, form.apellidos.data,
                                           form.celular.data, form.email.data, form.contrasena.data, form.nivel.data)
        login_user(empleado)
        return redirect(url_for(".index"))
    return render_template("auth/register.html", title="Registro", form=form)


@page.route("/logout")
def logout():
    logout_user()
    return redirect(url_for(".login"))


@page.route("/index")
@login_required
def index():
    return render_template("index.html", title="Sistema almacen", empleado=current_user)


@page.route("/inventario", methods=['GET', 'POST'])
@login_required
def productos():
    # producto = Producto.query
    if request.method == 'POST':
        form = SearchForm(request.form)
        if form.categoria.data == '0':
            _productos = Producto.query.filter(
                Producto.nombre.like(form.searched.data+"%")).all()
            lst = []
            for i in _productos:
                lst.append(i.id_tipo_producto)
            tipo_productos = TipoProducto.query.filter(
                TipoProducto.id.in_(lst)).all()
        else:
            tipo_productos = TipoProducto.query.where(
                TipoProducto.id == form.categoria.data).all()
            _productos = Producto.query.filter(
                Producto.nombre.like(form.searched.data + "%")).where(
                Producto.id_tipo_producto == tipo_productos[0].id).all()
        return render_template("task/admin/inventario.html", title="Inventario",
                               _productos=_productos, tipo_productos=tipo_productos, form=form)

    form = SearchForm()
    _productos = Producto.query.all()
    tipo_productos = TipoProducto.query.all()
    return render_template("task/admin/inventario.html", title="Inventario",
                           _productos=_productos, tipo_productos=tipo_productos, form=form)


@page.route("/solicitudes", methods=['GET', 'POST'])
@page.route("/solicitudes/<int:id>/<ope>", methods=['GET', 'POST'])
def solicitudes(id=None, ope=None):

    solicitud = SolicitudDetalle.get_by_id(id)
    if solicitud:
        if ope == "a":
            SolicitudDetalle.aceptar_solicitud(id)
        elif ope == "r":
            SolicitudDetalle.rechazar_solicitud(id)
        elif ope == "s":
            SolicitudDetalle.solicitar_nuevo(id)

    solicitud_empleados = (db.session.query(Solicitud, Empleado.nombres).join(Empleado, Solicitud.id_empleado
                                                                              == Empleado.id).group_by(Solicitud.id).all())

    solicitud_detalles = (db.session.query(SolicitudDetalle, Solicitud, Producto).join(Solicitud, SolicitudDetalle.id_solicitud ==
                                                                                       Solicitud.id).join(Producto, SolicitudDetalle.id_producto == Producto.id).group_by(SolicitudDetalle.id).all())
    return render_template("task/admin/solAprobadas.html", title="solAprobadas",
                           solicitud_detalle=solicitud_detalles)


@page.route('/search-despacho', methods=["POST"])
@login_required
def search_despacho():
    form = DespachoSearchForm()
    if form.validate_on_submit():
        despacho.searched = form.searched.data

        solicitud_detalles = (db.session.query(SolicitudDetalle, Solicitud, Producto).join(Solicitud, SolicitudDetalle.id_solicitud ==
                                                                                           Solicitud.id).join(Producto, SolicitudDetalle.id_producto == Producto.id
                                                                                                              ).filter(SolicitudDetalle.id == despacho.searched).all())

        return render_template("task/admin/search_despacho.html", form=form,
                               searched=despacho.searched, solicirudD=solicitud_detalles)


@page.route('/despacho', methods=["GET", "POST"])
@login_required
def despacho():
    form = DespachoSearchForm()
    title = "Despachos"
    if request.is_json:
        if len(request.args) > 1:
            ids_sd = []
            ids_sd.append(request.args['sol_de'])
            if ',' in request.args['sol_de']:
                ids_sd = request.args['sol_de'].split(',')
                ids_sd.pop()
            Salida.create(request.args['nombre'],
                          request.args['ci'], request.args['id'])
            for i in ids_sd:
                SolicitudDetalle.despachar_solicitud(i)
        searched = request.args['form']
        titulo_solicitud = Solicitud.query.filter_by(id=searched).first()
        solicitud_detalles = (db.session.query(SolicitudDetalle, Solicitud, Producto).join(
            Solicitud, SolicitudDetalle.id_solicitud == Solicitud.id).join(
            Producto, SolicitudDetalle.id_producto == Producto.id).where(
            SolicitudDetalle.id_solicitud == searched).where(
            SolicitudDetalle.estado == "A"))
        if titulo_solicitud != None:
            titulo_solicitud = titulo_solicitud.titulo
        else:
            titulo_solicitud = ''
        return jsonify({
            "text": render_template(
                "task/admin/search_despacho.html", form=form,
                searched=searched, solicirudD=solicitud_detalles,
                title=title, titulo_solicitud=titulo_solicitud
            )})
    return render_template("task/admin/despacho.html", form=form, title=title)


@page.route('/ingresos-salidas', methods=["GET"])
@login_required
def ingresos_salidas():
    form = EntradasSalidasForm()
    salidas = (db.session.query(Salida, Solicitud, SolicitudDetalle).join(
        Solicitud, Salida.id_solicitud == Salida.id).join(
        SolicitudDetalle, Salida.id_solicitudD == SolicitudDetalle.id))
    return render_template("task/admin/ingresos_salidas.html",
                           salidas=salidas, title="Ingresos y Salidas", form=form)


@page.route('/ingreso', methods=["GET", "POST"])
@page.route("/ingreso/<int:id>", methods=['GET', 'POST'])
def ingreso(id=None):
    titulo = "Entradas"
    form = entrada(request.form)
    if request.method == 'POST' and form.validate():
        solicitud = Ingreso.crear_ingresos(form.producto.data,
                                           form.cantidad.data, form.descripcion.data, form.precio_unitario.data,
                                           form.precio_total.data)
        return redirect(url_for(".index"))
    return render_template("task/admin/ingreso.html", title=titulo, form=form)


"""Empleados"""


@page.route('/empleados/solicitar', methods=["GET", "POST"])
@login_required
def solicitar():
    if request.is_json:
        if request.args['id_tp'] != "false":
            id_tp = request.args['id_tp']
            productos = Producto.query.filter_by(id_tipo_producto=id_tp).all()
            return jsonify({"text": render_template("task/empleado/list_productos.html",
                                                    productos=productos, cant=len(productos))})
        elif request.args['id_tp'] == "false":
            titulo = request.args['titulo']
            solicitud = Solicitud.create(titulo, current_user.id)

            cantidades = request.args['cantidades'].split("-")
            id_productos = request.args['id_productos'].split("-")
            cantidades.pop()
            id_productos.pop()
            for i, j in zip(cantidades, id_productos):
                SolicitudDetalle.create(i, "radifo", "P", solicitud, j)
            return jsonify({"text": "ok"})
        else:
            return jsonify({"text": "no exite prductos"})

    tipo_productos = TipoProducto.query.all()
    return render_template("task/empleado/solicitar.html", tipo_productos=tipo_productos, title="Solicitud de productos")


@page.route('/empleados/estado_solicitud', methods=["GET", "POST"])
@login_required
def estado_solicitud():
    salidas = (db.session.query(SolicitudDetalle, Solicitud, Producto).join(
        Solicitud, SolicitudDetalle.id_solicitud == Solicitud.id).join(
        Producto, SolicitudDetalle.id_producto == Producto.id).where(Solicitud.id_empleado == current_user.id))
    return render_template("task/empleado/estado_solicitud.html",
                           salidas=salidas, title="Ingresos y Salidas")
