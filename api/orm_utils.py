import json
from typing import List
from flask import abort, current_app
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
            detailed_abort(400, e)

    def get_or_none(self, *args, **kwargs):
        """Get single item - use when need there's need for custom action if searched entity does not exist"""
        try:
            return self.get(*args, **kwargs)
        except DoesNotExist:
            return None
        except ValidationError as e:
            detailed_abort(400, e)


class QuerySetCategoryExtended(QuerySetExtended):
    def delete(self, *args, **kwargs):
        """Checks extra conditions before allowing deletion of category"""
        try:
            # Actions in Try block require to try attempt to delete single, specific Category
            self_data_dict = json.loads(self.to_json())[0]
            if error_msg := self.check_any_parts_using_this_category(self_data_dict):
                detailed_abort(409, error_msg)
            if error_msg := self.check_child_categories_for_parts_using_them(
                self_data_dict
            ):
                detailed_abort(409, error_msg)

            super().delete(*args, **kwargs)
            self.readjust_subcategories_parent(self_data_dict)
        except IndexError:
            # When we try to delete all documents in collection, self_data_dict will be empty
            super().delete(*args, **kwargs)

    def check_any_parts_using_this_category(self, data):
        """Returns True, if there are parts assigned to this category, else returns False"""

        from api.models import Part

        name = data["name"]
        parts_count_with_this_category = Part.objects(category=name)
        if parts_count_with_this_category.count() > 0:
            return f"Deletion failed - there are parts using this category {name}"
        return None

    def check_child_categories_for_parts_using_them(self, data):
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
                error_msg = f"Deletion failed - part '{part_name}' is using this category or one of subcategories '{category_name}'."
                return error_msg
            else:
                # Check all children of this child category recursively, depth-first
                if error_msg := self.check_child_categories_for_parts_using_them(
                    child_data
                ):
                    return error_msg
        return None

    def readjust_subcategories_parent(self, self_data: dict):
        """
        In situation, where there is category A, its subcategory B, and Bs subcategory C -
        When B category is deleted, adjust C to use A as parent.
        self_data - dictionary from self.to_json() with data of current category
        """
        from api.models import Category

        parent_name = self_data["parent_name"]
        children = Category.objects(parent_name=self_data["name"])

        if parent_name:
            children.update(parent_name=parent_name)
            return

        children_list = self.get_all_children(category=self_data)

        # get all direct or indirect child category names of current category
        children = Category.objects(name__in=children_list)

        current_app.logger.debug(
            f"Deleting all children of category: {self_data["name"]}: {children_list}"
        )
        children.delete()

    def get_all_children(self, category: dict) -> List[str]:
        """Creates and returns list of all direct and indirect subcategory names."""
        from api.models import Category

        children_names = []
        direct_children = Category.objects(parent_name=category["name"])
        if direct_children:
            direct_children_names = [categ.name for categ in direct_children]
            children_names = children_names + direct_children_names

            indirect_children_names = []
            for child in direct_children:
                indirect_children_names = (
                    indirect_children_names + self.get_all_children(category=child)
                )
            children_names = children_names + indirect_children_names
        return children_names


class DynamicDocumentWithUtils(DynamicDocument):
    meta = {"abstract": True, "queryset_class": QuerySetExtended}


class DynamicDocumentCategory(DynamicDocument):
    meta = {"abstract": True, "queryset_class": QuerySetCategoryExtended}
