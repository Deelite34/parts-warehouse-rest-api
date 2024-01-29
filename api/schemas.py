from marshmallow import INCLUDE, Schema, fields, post_dump, ValidationError, validates
from api.models import Category, Part
from marshmallow.validate import Range


class KeepUnknowns:
    class Meta:
        # Workaround that keeps unknown fields through validations schema.load()
        unknown = INCLUDE

    @post_dump(pass_original=True)
    def keep_unknowns(self, output, orig, **kwargs):
        """
        Workaround that keeps unknown fields through validations schema.dump()
        https://github.com/marshmallow-code/marshmallow/issues/1545#issuecomment-1051943440
        """
        for key in orig:
            if key not in output:
                output[key] = orig[key]
        return output


class NestedLocationSchema(Schema):
    room = fields.String(required=True, allow_blank=True)
    bookcase = fields.String(required=True, allow_blank=True)
    shelf = fields.String(required=True, allow_blank=True)
    cuvette = fields.String(required=True, allow_blank=True)
    column = fields.String(required=True, allow_blank=True)
    row = fields.String(required=True, allow_blank=True)


class PartSchema(KeepUnknowns, Schema):
    serial_number = fields.String(required=True, unique=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    category = fields.String(required=True)
    quantity = fields.Integer(
        required=True,
        validate=Range(min_inclusive=1, error="Quantity must be greater than 0"),
    )
    price = fields.Float(
        required=True,
        validate=Range(min_inclusive=0.01, error="Price must be greater or equal 0.01"),
    )
    location = fields.Nested(NestedLocationSchema, required=True)

    @validates("serial_number")
    def serial_number_is_unique(self, value):
        """Gives structured json response with details if this validation fails"""
        field_name = "serial_number"
        serial_number_already_used = Part.objects.get_or_none(serial_number=value)
        if serial_number_already_used:
            raise ValidationError(
                f"Value '{value}' of unique field {field_name} is already in use."
            )

    @validates("category")
    def category_is_not_base_category(self, value):
        """Gives structured json response with details if this validation fails"""
        category = Category.objects.get_or_none(name=value)
        if not category:
            raise ValidationError(f"Category {value} does not exist.")
        if category.parent_name == "":
            raise ValidationError(
                "Category must not be a base category. Choose category that has non blank parent_name field."
            )


class PartSearchSchema(KeepUnknowns, Schema):
    id = fields.String()
    serial_number = fields.String()
    name = fields.String()
    description = fields.String()
    category = fields.String()
    quantity = fields.Integer(
        validate=Range(min_inclusive=1, error="Quantity must be greater than 0"),
    )
    price = fields.Float(
        validate=Range(min_inclusive=0.01, error="Price must be greater or equal 0.01"),
    )

    room = fields.String()
    bookcase = fields.String()
    shelf = fields.String()
    cuvette = fields.String()
    column = fields.String()
    row = fields.String()


class CategorySchema(KeepUnknowns, Schema):
    name = fields.String(required=True, unique=True)
    parent_name = fields.String(required=True, allow_blank=True)

    @validates("name")
    def category_name_is_unique(self, value):
        """Gives structured json response with details if this validation fails"""
        field_name = "name"
        name_already_used = Category.objects.get_or_none(name=value)
        if name_already_used:
            raise ValidationError(
                f"Value '{value}' of unique field {field_name} is already in use."
            )
