from mongoengine import StringField, FloatField, DictField, DynamicDocument, IntField

from queryset import QuerySetExtended


class DynamicDocumentWithUtils(DynamicDocument):
    meta = {"allow_inheritance": True, "queryset_class": QuerySetExtended}


class Part(DynamicDocumentWithUtils):
    serial_number = StringField(required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)
    location = DictField(required=True)


class Category(DynamicDocumentWithUtils):
    name = StringField(required=True)
    parent_name = StringField(required=True)
