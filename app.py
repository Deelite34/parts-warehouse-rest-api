import os
from flask import Flask

from config.settings import DevConfig, config_by_name
from manage import run_pytest
from api.routes import api_bp
from extensions import api
import mongoengine as me
from logging.config import dictConfig


def register_blueprints(app: Flask):
    with app.app_context():
        app.register_blueprint(api_bp)


def init_extensions(app: Flask):
    api.init_app(app)


def add_commands(app: Flask):
    app.cli.add_command(run_pytest)


def create_app():
    flask_app = Flask(__name__)
    config = config_by_name[os.environ["MODE"]]
    flask_app.config.from_object(config)

    dictConfig(flask_app.config["LOGGING_CONFIG"])

    register_blueprints(flask_app)
    init_extensions(flask_app)
    add_commands(flask_app)

    if config is DevConfig:
        me.connect("warehouse", host=flask_app.config["MONGODB_HOST"])
        flask_app.logger.debug(
            "Connected to local development 'warehouse' Mongo database."
        )

    return flask_app
