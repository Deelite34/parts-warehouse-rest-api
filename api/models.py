from mongoengine import Document, StringField, FloatField, DictField


class Part(Document):
    serial_number = StringField(required=True)
    name = StringField(required=True)
    desription = StringField(required=True)
    category = StringField(required=True)
    quantity = StringField(required=True)
    price = FloatField(required=True)
    location = DictField(required=True)


class Category(Document):
    name = StringField(required=True)
    parent_name = StringField(required=True)
