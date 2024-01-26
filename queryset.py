from flask import abort, make_response
from mongoengine.errors import DoesNotExist, ValidationError
from mongoengine.queryset import QuerySet


class QuerySetExtended(QuerySet):
    """Custom query helper methods"""

    def get_or_404(self, *args, **kwargs):
        """Gets item by id, on exception returns corresponding message"""
        try:
            return self.get(*args, **kwargs)
        except DoesNotExist:
            abort(404)
        except ValidationError as e:
            code = 400
            abort(
                make_response(
                    {"code": code, "status": "Bad Request", "details": str(e)}, code
                )
            )

    def get_or_none(self, *args, **kwargs):
        """Get single item - use when need there's need for custom action if searched entity does not exist"""
        try:
            return self.get(*args, **kwargs)
        except DoesNotExist:
            return None
        except ValidationError as e:
            code = 400
            abort(
                make_response(
                    {"code": code, "status": "Bad Request", "details": str(e)}, code
                )
            )
