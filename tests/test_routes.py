from flask import url_for
import mongoengine
from tests.conftest import SUBCATEGORY_NAME


def test_connection_to_test_db(app):
    assert mongoengine.connection.get_db().name == "test"


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
