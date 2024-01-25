import os
from flask import Flask

from config.settings import config_by_name
from manage import run_pytest
from blueprints import api_bp
from extensions import api


def register_blueprints(app: Flask):
    with app.app_context():
        app.register_blueprint(api_bp)


def init_extensions(app: Flask):
    api.init_app(app)


def add_commands(app: Flask):
    app.cli.add_command(run_pytest)


def create_app():
    flask_app = Flask(__name__)
    mode = os.getenv("mode")
    flask_app.config.from_object(config_by_name[mode])

    register_blueprints(flask_app)
    init_extensions(flask_app)
    add_commands(flask_app)

    return flask_app
