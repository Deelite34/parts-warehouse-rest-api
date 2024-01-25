import marshmallow as ma


class PartSchema(ma.Schema):
    serial_number = ma.fields.String(required=True)
    name = ma.fields.String(required=True)
    description = ma.fields.String(required=True)
    category = ma.fields.String(required=True)
    quantity = ma.fields.Integer(required=True)
    price = ma.fields.Float(required=True)
    location = ma.fields.Dict(required=True)


class CategorySchema(ma.Schema):
    name = ma.fields.String(required=True)
    parent_name = ma.fields.String(required=True, allow_blank=True)
