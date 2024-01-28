import os


class BaseConfig:
    MODE = os.getenv("MODE")
    API_TITLE = "Parts Warehouse API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"

    OPENAPI_URL_PREFIX = "/docs/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    LOGGING_CONFIG = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }


class ProdConfig(BaseConfig):
    SECRET_KEY = os.getenv("secret_key")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
    # TODO CONNECTION_STRING = f"mongodb+srv://{os.getenv("MONGODB_USERNAME")}:{os.getenv("MONGODB_PASSWORD")}@{os.getenv("MONGODB_CLUSTER")}"


class DevConfig(BaseConfig):
    DEBUG = True

    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
    MONGODB_HOST = "mongodb://mongodb/"
    CONNECTION_STRING = f"mongodb://mongodb/{MONGODB_DB_NAME}"

    LOGGING_CONFIG = dict(BaseConfig.LOGGING_CONFIG)  # Copy of parent config setting
    LOGGING_CONFIG["root"] = {"level": "DEBUG", "handlers": ["wsgi"]}


class TestConfig(DevConfig):
    """use only when creating flask app object in tests"""

    TESTING = True

    MONGODB_DB_NAME = "test"
    CONNECTION_STRING = f"mongodb://mongodb/{MONGODB_DB_NAME}"


config_by_name = {
    "production": ProdConfig,
    "development": DevConfig,
    "test": TestConfig,
}
