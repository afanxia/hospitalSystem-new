#! ../env/bin/python
import os
from flask import Flask

from flask_cors import CORS
from hospitalSystem.error import mappings
from hospitalSystem.models import db
from hospitalSystem import hook
#from hospitalSystem.controllers.user import bp as user_bp

from hospitalSystem.extensions import (
    babel,
    login_manager,
)

from flask_restplus import Api
from flask import Blueprint

from hospitalSystem.controllers.permission import perm_api
from hospitalSystem.controllers.user import user_api
from hospitalSystem.controllers.role import role_api
from hospitalSystem.controllers.auth import auth_api


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. hospitalSystem.settings.ProdConfig
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    for k, v in app.config.items():
        v2 = os.environ.get(k)
        if v2 is not None:
            app.config[k] = type(v)(v2)  # int('3'), bool('')
    babel.init_app(app)
    # initialize SQLAlchemy
    db.init_app(app)

    CORS(app)

    print('using', app.config['SQLALCHEMY_DATABASE_URI'])
    login_manager.init_app(app)
    # register our blueprints
    # app.register_blueprint(default_bp)

    blueprint = Blueprint('api', __name__)

    api = Api(blueprint,
              title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
              version='1.0',
              description='a boilerplate for flask restplus web service'
              )

    api.add_namespace(user_api, path='/users')
    api.add_namespace(role_api, path='/roles')
    api.add_namespace(perm_api, path='/permissions')
    api.add_namespace(auth_api, path='')
    app.register_blueprint(blueprint, url_prefix='/api')
    #app.register_blueprint(user_bp, url_prefix=app.config['API_VERSION'])

    for e, hdl in mappings:
        app.register_error_handler(e, hdl)

    if app.config.get('DEBUG', False):
        app.before_first_request(hook.before_first_req)
        app.before_request(hook.before_req)
        app.after_request(hook.after_req)

    return app
