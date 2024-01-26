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

    serial_number = StringField(required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)
    location = EmbeddedDocumentField(LocationDocument, required=True)


class Category(DynamicDocumentCategory):
    meta = {"collection": "categories"}

    name = StringField(required=True)
    parent_name = StringField(required=True)
