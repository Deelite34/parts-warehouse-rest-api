import utils
from api.models import Category, Part


def test_detailed_abort(mocker):
    mocker.patch("utils.abort")
    mocker.patch("utils.make_response")
    code = 418
    details = "I am teapot"

    utils.detailed_abort(code, details)
    make_response_args = utils.make_response.call_args.args[0]

    utils.abort.assert_called()
    utils.make_response.assert_called()
    expected_keys = ("code", "status", "details")
    assert all([key in make_response_args for key in expected_keys])
    assert make_response_args["details"] == details


def test_generate_data(mocker):
    """attempts to create specific amount of parts and categories"""
    mocker.patch("api.models.Part.objects")
    mocker.patch("api.models.Category.objects")

    utils.generate_sample_data()
    part_insert_args = Part.objects.insert.call_args.args[0]
    category_insert_args = Category.objects.insert.call_args.args[0]

    Part.objects.insert.assert_called_once()
    Category.objects.insert.assert_called_once()
    assert len(part_insert_args) == 6
    assert any(
        (len(category_insert_args) == 3, len(category_insert_args) == 4)
    )  # With or without base category
