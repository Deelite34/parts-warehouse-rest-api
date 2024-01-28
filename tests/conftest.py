import pytest
import mongoengine as me
from api.models import Category, Part
from app import create_app


BASE_CATEGORY_NAME = "test_base_category"
SUBCATEGORY_NAME = "test_items_category"


@pytest.fixture(scope="session")
def app():
    """Uses 'test' database for tests"""
    me.disconnect()
    app = create_app(testing=True)

    app_context = app.test_request_context()
    app_context.push()

    yield app

    # cleanup

    me.disconnect()
    app_context.pop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def setup_cleanup_before_and_after_each_test():
    """Set up and cleanup after each test"""
    base_category = Category(name=BASE_CATEGORY_NAME, parent_name="")
    subcategory = Category(name=SUBCATEGORY_NAME, parent_name=BASE_CATEGORY_NAME)
    base_category.save()
    subcategory.save()

    yield

    Part.objects.delete()
    Category.objects.delete()
