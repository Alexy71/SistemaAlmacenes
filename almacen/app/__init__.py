from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

db = SQLAlchemy()
csrf = CSRFProtect()
bootstrap = Bootstrap()
login_manager = LoginManager()

from .conts import LOGIN_REQUIRED
from .models import *
from .seeds import *
from .views import page


def create_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    
    if not app.config.get('TEST', False):
        bootstrap.init_app(app)
        
    app.app_context().push()
    
    login_manager.init_app(app)
    login_manager.login_view=".login"
    login_manager.login_message_category = "error"
    login_manager.login_message = LOGIN_REQUIRED
    app.register_blueprint(page)

    with app.app_context():
        db.init_app(app)    
        db.create_all()

    return app
