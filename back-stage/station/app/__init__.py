import datetime

from flask_cors import CORS
from flask import Flask

from app.libs.redis import redis_client
from app.models import db, ma
from app.token import jwt
# from app.cache import cache
from app.config.config import config_ini


def register_blueprints(_app):
    from app.api.m2 import create_blueprint_m2
    _app.register_blueprint(create_blueprint_m2(), url_prefix='/m2')


def create_app():
    app = Flask(__name__, template_folder='../templates')

    CORS(app, resources={r'/*': {'origins': '*'}})

    app.config['SQLALCHEMY_DATABASE_URI'] = config_ini['server']['DATABASE_URL']
    app.config['SECRET_KEY'] = config_ini['server']['SECRET_KEY']
    app.config['MAX_CONTENT_LENGTH'] = int(config_ini['uploads']['UPLOAD_IMG_MAX_SIZE'])
    app.config['JWT_SECRET_KEY'] = config_ini['jwt']['JWT_SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(
        minutes=int(config_ini['jwt']['JWT_ACCESS_TOKEN_EXPIRES']))
    app.config['JWT_HEADER_NAME'] = config_ini['jwt']['JWT_HEADER_NAME']
    app.config['JWT_HEADER_TYPE'] = config_ini['jwt']['JWT_HEADER_TYPE']
    app.config['REDIS_URL'] = config_ini['server']['REDIS_URL']

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)
    register_blueprints(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
