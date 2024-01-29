import os
from flask import Flask

from config.settings import ProdConfig, config_by_name
from api.routes import api_bp
from extensions import api
import mongoengine as me
from logging.config import dictConfig
from manage import create_data, run_pytest


def register_blueprints(app: Flask):
    with app.app_context():
        api.register_blueprint(api_bp)


def init_extensions(app: Flask):
    api.init_app(app)


def add_commands(app: Flask):
    app.cli.add_command(create_data)
    app.cli.add_command(run_pytest)


def create_app(testing=False):
    flask_app = Flask(__name__)

    if not testing:
        config = config_by_name[os.environ["MODE"]]
    else:
        config = config_by_name["test"]
    flask_app.config.from_object(config)

    dictConfig(flask_app.config["LOGGING_CONFIG"])

    init_extensions(flask_app)
    register_blueprints(flask_app)
    add_commands(flask_app)

    db = flask_app.config["MONGODB_DB_NAME"]
    if config is not ProdConfig:
        host = flask_app.config["MONGODB_HOST"]
        me.connect(db=db, host=host)

        mode = flask_app.config["MODE"]
        flask_app.logger.debug(
            f"Connected to local {mode} {flask_app.config['MONGODB_DB_NAME']} Mongo database."
        )
    else:
        host = flask_app.config["CONNECTION_STRING"]
        me.connect(db=db, host=host)

        flask_app.logger.debug("Connected to production database.")
    return flask_app
