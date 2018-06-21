import os

import redis
from flask import Flask
from flask_session import Session

from APP.house_views import house_blueprint
from APP.models import db
from APP.user_veiws import user_blueprint
from utils.setting import BASE_DIR

se = Session()


def create_app():

    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        "mysql+pymysql://root:123456@localhost:3306/jiajuflask"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

    #初始化
    se.init_app(app=app)
    db.init_app(app=app)
    return app