from flask_sqlalchemy import SQLAlchemy


class Config:
    SECRET_KEY = "secret"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/SistemaAlmacen"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/SistemaAlmacen"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/TestSistemaAlmacen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    TESTING = True
    TEST = True


configuraciones = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
    "product": ProductConfig,
    "test": TestConfig
}
