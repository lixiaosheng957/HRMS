from flask import Flask
from config import config
from app.models.base import db
from flask_cors import CORS
from app.timed_task import scheduler
from app.libs.status_code import Success


def register_blueprints(app):
    from app.api import create_blueprint
    app.register_blueprint(create_blueprint(), url_prefix='/api')


def register_plugin(app):
    db.init_app(app)
    db.app = app
    CORS(app)
    scheduler.init_app(app)
    import app.timed_task.check_traning_program_end
    import app.timed_task.change_work_age
    scheduler.start()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    register_plugin(app)
    register_blueprints(app)
    return app
