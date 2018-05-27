import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'replace-this-with-some-other-string'
    BABEL_DEFAULT_LOCALE = 'zh'
    SESSION_COOKIE_NAME = 'hospitalSystem'
    DEBUG = False
    # WTF_CSRF_ENABLED = False
    # SQLALCHEMY_ECHO = True  # comment out to log sql statement
    API_VERSION = ''
    #SQLALCHEMY_DATABASE_URI = ( 'mysql+pymysql://root:asdfasdf@localhost:3306/hospitalSystem?charset=utf8mb4')

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    #DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:asdfasdf@localhost:3306/hospitalSystem?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    #DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:asdfasdf@localhost:3306/hospitalSystemTesting?charset=utf8mb4'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
