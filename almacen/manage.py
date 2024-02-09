from venv import create

from flask_migrate import Migrate, MigrateCommand
from flask_script import Command, Manager, Shell

from app import (Empleado, Ingreso, Producto, Salida, Solicitud,
                 SolicitudDetalle, TipoProducto, create_app, db)
from app.seeds import seed_all, seed_empleado, seed_solicitud, seed_solicitudD
from config import *

config_class = configuraciones["product"]
app = create_app(config_class)
migrate = Migrate(app, db)


class seed(Command):
    def run(self):
        seed_all()


def make_shell_context():
    return dict(app=app, db=db, Empleado=Empleado, Producto=Producto,
                TipoProducto=TipoProducto, SolicitudDetalle=SolicitudDetalle,
                Ingreso=Ingreso, Salida=Salida)


if __name__ == "__main__":
    manager = Manager(app)
    manager.add_command('shell', Shell(make_context=make_shell_context))

    manager.add_command('db', MigrateCommand)
    manager.add_command('seed', seed())

    @manager.command
    def test():
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner().run(tests)

    manager.run()
