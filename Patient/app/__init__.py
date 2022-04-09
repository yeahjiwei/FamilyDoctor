from flask import Flask
from . import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    from .views.index import index_blueprint
    app.register_blueprint(index_blueprint)  # 注册蓝图

    return app

