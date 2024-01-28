from api.models import Category
from tests.conftest import BASE_CATEGORY_NAME, SUBCATEGORY_NAME
from api import orm_utils
from tests.factories import make_part


def test_querysetextended_get_or_404(mocker):
    name = SUBCATEGORY_NAME + "123"
    category = Category(name=name, parent_name=BASE_CATEGORY_NAME)
    category.save()

    result = Category.objects.get_or_404(name=name)

    assert result.name == name


def test_querysetextended_get_or_404_missing_error(mocker):
    mocker.patch("api.orm_utils.abort")

    result = Category.objects.get_or_404(name="somename345")

    orm_utils.abort.assert_called()
    assert not result


def test_querysetextended_get_or_none(mocker):
    mocker.patch("api.orm_utils.detailed_abort")

    result = Category.objects.get_or_none(id="somename345")

    assert result is None


def test_querysetextended_check_any_parts_using_this_category(mocker):
    mocker.patch("api.orm_utils.detailed_abort")
    name = SUBCATEGORY_NAME + "123"
    category = Category(name=name, parent_name=BASE_CATEGORY_NAME)
    category.save()
    make_part(category_name=name)

    category.delete()

    orm_utils.detailed_abort.assert_called_with(
        409, f"Deletion failed - there are parts using this category {name}"
    )


def test_querysetextended_check_child_category_for_parts_using_it(mocker):
    mocker.patch("api.orm_utils.detailed_abort")
    name_1 = SUBCATEGORY_NAME + "1"
    name_2 = SUBCATEGORY_NAME + "2"
    name_3 = SUBCATEGORY_NAME + "3"
    category_1 = Category(name=name_1, parent_name=BASE_CATEGORY_NAME)
    category_1.save()
    category_2 = Category(name=name_2, parent_name=category_1.name)
    category_2.save()
    category_3 = Category(name=name_3, parent_name=category_2.name)
    category_3.save()
    part = make_part(category_name=category_3.name)[0]

    category_1.delete()

    orm_utils.detailed_abort.assert_called_with(
        409,
        f"Deletion failed - part '{part.name}' is using this category or one of subcategories '{category_2.name}'.",
    )
