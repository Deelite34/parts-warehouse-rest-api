import json
from flask_smorest import Blueprint
from flask.views import MethodView

from api.schemas import CategorySchema, PartSchema
from api.models import Category, Part

api_bp = Blueprint("api", __name__, url_prefix="/api/v1/")


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
