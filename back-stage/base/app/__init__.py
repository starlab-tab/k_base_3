from flask_cors import CORS
from flask import Flask

from app.models import db


def register_blueprints(_app):
    from app.api.v2 import create_blueprint_v2
    _app.register_blueprint(create_blueprint_v2(), url_prefix='/v2')


def register_plugin(app):
    pass


def create_app():
    app = Flask(__name__, template_folder='../templates')

    CORS(app, resources={r'/*': {'origins': '*'}})

    from app.config.config import config_ini
    app.config['SQLALCHEMY_DATABASE_URI'] = config_ini['server']['database_url']
    db.init_app(app)
    register_blueprints(app)
    # 必须再app上下文环境才能完成操作
    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app
