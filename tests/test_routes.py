from flask import url_for
import mongoengine
from tests.conftest import BASE_CATEGORY_NAME, SUBCATEGORY_NAME
from tests.factories import make_category, make_part


def test_connection_to_test_db(app):
    assert mongoengine.connection.get_db().name == "test"


def test_part_get_many(app, client):
    make_category(count=1)[0]
    make_part(count=3)

    response = client.get(
        url_for("api.Parts"),
    )

    assert response.status_code == 200
    assert len(response.json) == 3
    assert all([isinstance(i, dict) for i in response.json])


def test_part_get(app, client):
    make_category(count=1)
    parts = make_part(count=1)
    part_id = parts[0].id

    response = client.get(
        url_for("api.PartsById", part_id=part_id),
    )

    assert response.status_code == 200
    assert response.json.get("category") == SUBCATEGORY_NAME


def test_part_create(app, client):
    serial_number = "s0m3-numb3r"

    response = client.post(
        url_for("api.Parts"),
        json={
            "serial_number": "s0m3-numb3r",
            "name": "Very good pc",
            "description": "Top quality pc with great components for gaming.",
            "category": SUBCATEGORY_NAME,
            "quantity": 1,
            "price": 7499,
            "location": {
                "room": "15",
                "bookcase": "21",
                "shelf": "2",
                "cuvette": "2",
                "column": "1",
                "row": "1",
            },
        },
    )

    assert response.status_code == 201
    assert serial_number in response.json.values()


def test_part_update_part_exists(app, client):
    make_category(count=1)
    parts = make_part(count=1)
    part_id = parts[0].id

    response = client.put(
        url_for("api.PartsById", part_id=part_id),
        json={
            "serial_number": "s0m3-numb3r123",
            "name": "Very good pc123",
            "description": "Top quality pc with great components for gaming.123",
            "category": SUBCATEGORY_NAME,
            "quantity": 1123,
            "price": 7499,
            "location": {
                "room": "15",
                "bookcase": "21",
                "shelf": "2",
                "cuvette": "2",
                "column": "1",
                "row": "1",
            },
        },
    )

    assert response.status_code == 200
    assert "123" in response.json.get("serial_number")


def test_part_update_part_does_not_exist(app, client):
    make_category(count=1)
    part_id = "1" * 24

    response = client.put(
        url_for("api.PartsById", part_id=part_id),
        json={
            "serial_number": "s0m3-numb3r123",
            "name": "Very good pc123",
            "description": "Top quality pc with great components for gaming.123",
            "category": SUBCATEGORY_NAME,
            "quantity": 1123,
            "price": 7499,
            "location": {
                "room": "15",
                "bookcase": "21",
                "shelf": "2",
                "cuvette": "2",
                "column": "1",
                "row": "1",
            },
        },
    )

    assert response.status_code == 200
    assert "123" in response.json.get("serial_number")


def test_part_delete(app, client):
    make_category(count=1)
    parts = make_part(count=1)
    part_id = parts[0].id

    response = client.delete(
        url_for("api.PartsById", part_id=part_id),
    )

    assert response.status_code == 204


def test_category_get(app, client):
    categories = make_category(count=1)
    category = categories[0]

    response = client.get(
        url_for("api.CategoriesById", category_id=category.id),
    )

    assert response.status_code == 200
    assert category.name == response.json.get("name")


def test_category_get_many(app, client):
    make_category(count=3)

    response = client.get(
        url_for("api.Categories"),
    )

    assert response.status_code == 200
    assert (
        len(response.json) == 5
    )  # 3 categories we created + 2 created in fixture on setup
    assert all([isinstance(i, dict) for i in response.json])


def test_category_create(app, client):
    new_category_name = "somename"

    response = client.post(
        url_for("api.Categories"),
        json={"name": new_category_name, "parent_name": BASE_CATEGORY_NAME},
    )

    assert response.status_code == 201
    assert response.json.get("name") == new_category_name


def test_category_update_category_exists(app, client):
    categories = make_category(count=1)
    category_id = categories[0].id

    response = client.put(
        url_for("api.CategoriesById", category_id=category_id),
        json={"name": "123", "parent_name": BASE_CATEGORY_NAME},
    )

    assert response.status_code == 200
    assert "123" in response.json.get("name")


def test_category_update_category_does_not_exist(app, client):
    new_category_name = "somename"
    category_id = "1" * 24

    response = client.put(
        url_for("api.CategoriesById", category_id=category_id),
        json={"name": new_category_name, "parent_name": BASE_CATEGORY_NAME},
    )

    assert response.status_code == 200
    assert response.json.get("name") == new_category_name


def test_category_delete(app, client):
    categories = make_category(count=1)
    category_id = categories[0].id

    response = client.delete(
        url_for("api.CategoriesById", category_id=category_id),
    )

    assert response.status_code == 204


def test_post_request_validation_part_schema_bad_fields(app, client):
    expected_detected_wrong_fields = [
        "category",
        "description",
        "location",
        "name",
        "serial_number",
    ]

    response = client.post(
        url_for("api.Parts"),
        json={
            "serial_number": 123,
            "name": 123,
            "description": 123,
            "category": "qwe",
            "quantity": 0,
            "price": 0,
            "location": {
                "room": 123,
                "bookcase": 123,
                "shelf": 123,
                "cuvette": 123,
                "column": 123,
                "row": 123,
            },
            "some_additional_field": "qwe",
        },
    )

    assert response.status_code == 422
    assert all(
        [
            _ in response.json.get("errors").get("json").keys()
            for _ in expected_detected_wrong_fields
        ]
    )


def test_post_request_validation_part_schema_missing_fields(app, client):
    expected_detected_wrong_fields = [
        "category",
        "description",
        "location",
        "name",
        "serial_number",
    ]

    response = client.post(
        url_for("api.Parts"),
        json={},
    )

    assert response.status_code == 422
    assert all(
        [
            _ in response.json.get("errors").get("json").keys()
            for _ in expected_detected_wrong_fields
        ]
    )


def test_post_request_validation_part_schema_serial_number_already_used(app, client):
    for _ in range(2):
        response = client.post(
            url_for("api.Parts"),
            json={
                "serial_number": "s0m3-numb3r",
                "name": "Very good pc",
                "description": "Top quality pc with great components for gaming.",
                "category": SUBCATEGORY_NAME,
                "quantity": 1,
                "price": 7499,
                "location": {
                    "room": "15",
                    "bookcase": "21",
                    "shelf": "2",
                    "cuvette": "2",
                    "column": "1",
                    "row": "1",
                },
            },
        )

    assert response.status_code == 422
    assert "serial_number" in response.json.get("errors").get("json").keys()


def test_post_request_validation_part_schema_category_does_not_exist(app, client):
    response = client.post(
        url_for("api.Parts"),
        json={
            "serial_number": "s0m3-numb3r",
            "name": "Very good pc",
            "description": "Top quality pc with great components for gaming.",
            "category": "wqeqwe",
            "quantity": 1,
            "price": 7499,
            "location": {
                "room": "15",
                "bookcase": "21",
                "shelf": "2",
                "cuvette": "2",
                "column": "1",
                "row": "1",
            },
        },
    )

    assert response.status_code == 422
    assert "category" in response.json.get("errors").get("json").keys()


def test_post_request_validation_category_schema_category_name_already_used(
    app, client
):
    for _ in range(2):
        response = client.post(
            url_for("api.Categories"),
            json={"name": "somename", "parent_name": BASE_CATEGORY_NAME},
        )

    assert response.status_code == 422
    assert "name" in response.json.get("errors").get("json").keys()
