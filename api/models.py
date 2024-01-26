from mongoengine import StringField, FloatField, DictField, IntField

from .orm_utils import DynamicDocumentCategory, DynamicDocumentWithUtils


class Part(DynamicDocumentWithUtils):
    serial_number = StringField(required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)
    location = DictField(required=True)


class Category(DynamicDocumentCategory):
    name = StringField(required=True)
    parent_name = StringField(required=True)
