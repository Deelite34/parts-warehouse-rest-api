import decimal
from mongoengine import (
    StringField,
    FloatField,
    IntField,
    EmbeddedDocument,
    EmbeddedDocumentField,
)

from .orm_utils import DynamicDocumentCategory, DynamicDocumentWithUtils


class LocationDocument(EmbeddedDocument):
    room = StringField(default="")
    bookcase = StringField(default="")
    shelf = StringField(default="")
    cuvette = StringField(default="")
    column = StringField(default="")
    row = StringField(default="")


class Part(DynamicDocumentWithUtils):
    meta = {"collection": "parts"}

    serial_number = StringField(required=True, unique=True)
    name = StringField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    quantity = IntField(required=True, min_value=1)
    # Maybe it should be considered, to consider additional warning in request response
    # if the price gets rounded
    price = FloatField(
        required=True, min_value=0.01, rounding=decimal.ROUND_UP
    )  # if rounding happens, company earns additional +-0.01 instead of losing +-0.01 per item
    location = EmbeddedDocumentField(LocationDocument, required=True)


class Category(DynamicDocumentCategory):
    meta = {"collection": "categories"}

    name = StringField(required=True, unique=True)
    parent_name = StringField(required=True)
