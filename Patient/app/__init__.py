from flask import Flask
from . import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    # 注册蓝图
    from .views.index import index_blueprint
    app.register_blueprint(index_blueprint)
    from .views.doctor_info import doctor_info_blueprint
    app.register_blueprint(doctor_info_blueprint)
    from .views.doctorDatabase import doctorDatabase_blueprint
    app.register_blueprint(doctorDatabase_blueprint)

    return app

