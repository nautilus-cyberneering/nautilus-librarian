from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.validate_filepaths_action import (
    validate_filepaths_action,
)


def given_a_dvc_diff_object_it_should_validate_the_filepath_of_the_new_media_files():

    dvc_diff_with_added_gold_image = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = validate_filepaths_action(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text("000001-32.600.2.tif ✓")


def given_a_dvc_diff_object_it_should_not_validate_the_filepath_of_the_modified_media_files():

    dvc_diff_with_modified_image = {
        "added": [],
        "deleted": [],
        "modified": [
            {"path": "data/000002/32/000002-32.600.2.tif"},
        ],
        "renamed": [],
    }

    result = validate_filepaths_action(compact_json(dvc_diff_with_modified_image))

    assert result.code == ResultCode.CONTINUE
    assert not result.contains_text("000002-32.600.2.tif ✓")


def given_a_dvc_diff_object_it_should_validate_the_filepath_of_the_renamed_media_files():

    dvc_diff_with_renamed_image = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [
            {
                "path": {
                    "old": "data/000001/32/000001-32.600.2.tif",
                    "new": "data/000002/32/000002-32.600.2.tif",
                }
            }
        ],
    }

    result = validate_filepaths_action(compact_json(dvc_diff_with_renamed_image))

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text("000002-32.600.2.tif ✓")
    assert not result.contains_text("000001-32.600.2.tif ✓")


def given_a_wrong_media_filepath_it_should_show_an_error():

    dvc_diff_with_wrong_filepath = {
        "added": [
            {"path": "data/000001/9999999/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = validate_filepaths_action(compact_json(dvc_diff_with_wrong_filepath))

    expected_message = """
        data/000001/9999999/000001-32.600.2.tif ✗ Invalid folder for image. The file \"data/000001/9999999/000001-32.600.2.tif\" should be in the folder \"data/000001/32\"
    """  # noqa

    assert result.code == ResultCode.ABORT
    assert expected_message.strip() == result.last_message_text()
