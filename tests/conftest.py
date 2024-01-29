import os
import pytest
import mongoengine as me
from api.models import Category, Part
from app import create_app
from config.settings import config_by_name
from mongoengine.connection import get_db

BASE_CATEGORY_NAME = "test_base_category"
SUBCATEGORY_NAME = "test_items_category"


@pytest.fixture()
def db():
    return get_db()


@pytest.fixture(scope="session", autouse=True)
def app():
    """Uses 'test' database for tests"""

    ### Setup
    me.disconnect_all()  # disconnect from main db
    app = create_app(testing=True)  # test app will connect to test db

    app_context = app.test_request_context()
    app_context.push()

    yield app

    ### teardown ###
    # Disconnect from test db
    me.disconnect_all()
    app_context.pop()

    # Reconnect to main database
    config = config_by_name[os.environ["MODE"]]
    db = config.MONGODB_DB_NAME
    host = config.MONGODB_HOST
    me.connect(db=db, host=host)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def db_cleanup_after_each_test():
    """Set up and cleanup after each test"""

    yield

    # Clean db after each test
    Part.objects.delete()
    Category.objects.delete()
