import json
from flask_smorest import Blueprint
from flask.views import MethodView

from api.schemas import PartSchema
from api.models import Part

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
        part = Part(**part)
        part.save()
        return json.loads(part.to_json())


@api_bp.route("/parts/<string:part_id>/")
class PartsById(MethodView):
    @api_bp.response(200, PartSchema)
    def get(self, part_id):
        part = Part.objects.get_or_404(id=part_id)
        return json.loads(part.to_json())

    # @api_bp.arguments(PartSchema, location="json")
    # @api_bp.response(201, PartSchema)
    def put(self, put_data, part_id):
        return {"Part": "updated part"}

    # @api_bp.response(204)
    def delete(self, part_id):
        return {"Part": "part deleted"}


@api_bp.route("/categories/")
class Categories(MethodView):
    # @api_bp.response(200, CategorySchema(many=True))
    def get(self):
        """List Parts"""
        return {"Part": "Sample info on Part"}

    # @api_bp.response(201, CategorySchema)
    def post(self):
        return {"Part": "create a Part"}


@api_bp.route("/categories/<string:category_id>/")
class CategoriesById(MethodView):
    # @api_bp.arguments(CategorySchema, location="json")
    # @api_bp.response(201, CategorySchema)
    def put(self):
        return {"Category": "updated Category"}

    # @api_bp.response(204)
    def delete(self):
        return {"Category": "Category deleted"}
