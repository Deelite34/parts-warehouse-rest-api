import os


class BaseConfig:
    API_TITLE = "Parts Warehouse API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"


class ProdConfig(BaseConfig):
    SECRET_KEY = os.getenv("secret_key")


class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    # MONGO_URI = f"mongodb://{os.getenv("MONGODB_USERNAME")}@:27017/{os.getenv("MONGODB_DATABASE")}"
    SECRET_KEY = "very12312secret!key"


class TestConfig(DevConfig):
    """use only when creating flask app object in tests"""

    DEBUG = True
    TESTING = True


config_by_name = {
    "production": ProdConfig,
    "development": DevConfig,
    "test": TestConfig,
}
