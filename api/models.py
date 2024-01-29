import decimal
from mongoengine import (
    StringField,
    FloatField,
    IntField,
    EmbeddedDocument,
    EmbeddedDocumentField,
)

from .orm_utils import DynamicDocumentCategory, DynamicDocumentWithUtils


class Location(EmbeddedDocument):
    room = StringField(default="", min_value=1)
    bookcase = StringField(default="", min_value=1)
    shelf = StringField(default="", min_value=1)
    cuvette = StringField(default="", min_value=1)
    column = StringField(default="", min_value=1)
    row = StringField(default="", min_value=1)


class Part(DynamicDocumentWithUtils):
    # Additional unknown fields are allowed, but not used by app
    meta = {"collection": "parts"}

    serial_number = StringField(required=True, unique=True)
    name = StringField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    quantity = IntField(required=True, min_value=1)
    price = FloatField(required=True, min_value=0.01, rounding=decimal.ROUND_UP)
    location = EmbeddedDocumentField(Location, required=True)


class Category(DynamicDocumentCategory):
    # Additional unknown fields are allowed, but not used by app
    meta = {"collection": "categories"}

    name = StringField(required=True, unique=True)
    parent_name = StringField(required=True)
