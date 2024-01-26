import json
from flask import abort
from mongoengine.errors import DoesNotExist, ValidationError
from mongoengine.queryset import QuerySet

from mongoengine import DynamicDocument

from utils import detailed_abort


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
            detailed_abort(code, e)

    def get_or_none(self, *args, **kwargs):
        """Get single item - use when need there's need for custom action if searched entity does not exist"""
        try:
            return self.get(*args, **kwargs)
        except DoesNotExist:
            return None
        except ValidationError as e:
            code = 400
            detailed_abort(code, e)


class QuerySetCategoryExtended(QuerySetExtended):
    def delete(self, *args, **kwargs):
        """Extra conditions before allowing deletion of category"""
        self_data_dict = json.loads(self.to_json())[0]

        if error_msg := self.check_any_parts_using_this_category(self_data_dict):
            detailed_abort(409, error_msg)
        if error_msg := self.check_child_category_for_parts_using_it(self_data_dict):
            detailed_abort(409, error_msg)

        super().delete(*args, **kwargs)

    def check_any_parts_using_this_category(self, data):
        """Returns True, if there are parts assigned to this category, else returns False"""

        from api.models import Part

        name = data["name"]
        parts_count_with_this_category = Part.objects(category=name)
        if parts_count_with_this_category.count() > 0:
            return f"Deletion failed - there are parts using this category {name}"
        return None

    def check_child_category_for_parts_using_it(self, data):
        """
        Returns string containing error message,
        if category has any child categories being used by any part,
        otherwise returns None
        """
        from api.models import Part, Category

        category_name = data["name"]
        child_categories = Category.objects(parent_name=category_name)

        if child_categories.count() == 0:
            return
        for child_category in child_categories:
            child_data = json.loads(child_category.to_json())
            child_category_name = child_data["name"]
            part_using_this_category = Part.objects(category=child_category_name)
            if part_using_this_category.count() > 0:
                part = json.loads(part_using_this_category[0].to_json())
                part_name = part["name"]
                error_msg = f"Deletion failed - part '{part_name}' is using this category or one of subcategories '{category_name}.'"
                return error_msg
            else:
                # Check all children of this child category recursively, depth-first
                if error_msg := self.check_child_category_for_parts_using_it(
                    child_data
                ):
                    return error_msg
        return None


class DynamicDocumentWithUtils(DynamicDocument):
    meta = {"abstract": True, "queryset_class": QuerySetExtended}


class DynamicDocumentCategory(DynamicDocument):
    meta = {"abstract": True, "queryset_class": QuerySetCategoryExtended}
