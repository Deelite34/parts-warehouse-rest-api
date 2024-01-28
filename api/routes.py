from ast import Dict
import json
from flask.views import MethodView
from marshmallow import INCLUDE

from api.schemas import CategorySchema, PartSchema, PartSearchSchema
from api.models import Category, Part
from flask_smorest import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api/v1/")
optional_part_schema = PartSchema(partial=True, unknown=INCLUDE)


@api_bp.route("/parts/")
class Parts(MethodView):
    @api_bp.response(200, PartSchema(many=True))
    def get(self):
        parts = Part.objects
        return json.loads(parts.to_json())

    @api_bp.arguments(PartSchema, location="json")
    @api_bp.response(201, PartSchema)
    def post(self, part):
        new_part = Part(**part)
        new_part.save()
        return json.loads(new_part.to_json())


@api_bp.route("/parts/<string:part_id>/")
class PartsById(MethodView):
    @api_bp.response(200, PartSchema)
    def get(self, part_id):
        part = Part.objects.get_or_404(id=part_id)
        return json.loads(part.to_json())

    @api_bp.arguments(PartSchema, location="json")
    @api_bp.response(200, PartSchema)
    def put(self, part, part_id):
        part_found = Part.objects.get_or_none(id=part_id)
        if not part_found:
            created_part = Part(**part)
            created_part.save()
            return json.loads(created_part.to_json())
        updated_part = Part.objects(id=part_id).modify(**part)
        return json.loads(updated_part.reload().to_json())

    @api_bp.response(204)
    def delete(self, part_id):
        part = Part.objects.get_or_404(id=part_id)
        part.delete()


@api_bp.route("/parts/search/")
class PartSearch(MethodView):
    @api_bp.arguments(PartSearchSchema, location="query")
    @api_bp.response(200, PartSchema(many=True))
    def get(self, args):
        updated_args = PartSearch.flatten_part_dict(args)
        parts = Part.objects(**updated_args)
        return json.loads(parts.to_json())

    @staticmethod
    def flatten_part_dict(part: Dict) -> Dict:
        """
        Flattens Part dictionary containing embedded location dict and converts location keys structure.
        As result, Part dictionary can be unpacked, and Part can be searched by location fields.
        Example:
        Part dict contains embedded dict {"shelf": 5}. Calling this func gives us flattened Part dict:
        {
        ...,
        'location__shelf': 5,
        }
        """

        embedded_location_fields = [
            "room",
            "bookcase",
            "shelf",
            "cuvette",
            "column",
            "row",
        ]

        if any([_ in part.keys() for _ in embedded_location_fields]):
            updated_args = dict(part)
            for key in part:
                # rename location specific keys to use "location__" prefix
                if key in embedded_location_fields:
                    try:  # attempt to convert possible number in str format, of shelf, row etc. to int
                        field = int(updated_args[key])
                    except ValueError:
                        field = updated_args[key]
                    finally:
                        updated_args.pop(key)
                    updated_args[f"location__{key}"] = field
            return updated_args
        return part


@api_bp.route("/categories/")
class Categories(MethodView):
    @api_bp.response(200, CategorySchema(many=True))
    def get(self):
        categories = Category.objects
        return json.loads(categories.to_json())

    @api_bp.arguments(CategorySchema, location="json")
    @api_bp.response(201, CategorySchema)
    def post(self, category):
        new_category = Category(**category)
        new_category.save()
        return json.loads(new_category.to_json())


@api_bp.route("/categories/<string:category_id>/")
class CategoriesById(MethodView):
    @api_bp.response(200, CategorySchema)
    def get(self, category_id):
        category = Category.objects.get_or_404(id=category_id)
        return json.loads(category.to_json())

    @api_bp.arguments(CategorySchema, location="json")
    @api_bp.response(200, CategorySchema)
    def put(self, category, category_id):
        category_found = Category.objects.get_or_none(id=category_id)
        if not category_found:
            created_category = Category(**category)
            created_category.save()
            return json.loads(created_category.to_json())
        updated_category = Category.objects(id=category_id).modify(**category)
        return json.loads(updated_category.reload().to_json())

    @api_bp.response(204)
    def delete(self, category_id):
        category = Category.objects.get_or_404(id=category_id)
        category.delete()
