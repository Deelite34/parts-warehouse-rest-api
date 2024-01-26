from marshmallow import INCLUDE, Schema, fields, post_dump


class KeepUnknownsSchema(Schema):
    class Meta:
        # This keeps unknown fields through schema.load(), but not schema.dump()
        unknown = INCLUDE

    @post_dump(pass_original=True)
    def keep_unknowns(self, output, orig, **kwargs):
        """
        Workaround that will allow us to keep unknown values through schema.dump()
        https://github.com/marshmallow-code/marshmallow/issues/1545#issuecomment-1051943440
        """
        for key in orig:
            if key not in output:
                output[key] = orig[key]
        output.pop("_cls")
        return output


class PartSchema(KeepUnknownsSchema):
    serial_number = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    category = fields.String(required=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    location = fields.Dict(required=True)


class CategorySchema(KeepUnknownsSchema):
    name = fields.String(required=True)
    parent_name = fields.String(required=True, allow_blank=True)
