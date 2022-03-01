from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.check_images_changes import (
    check_images_changes,
)


def given_a_diff_structure_with_no_changes_it_should_return_an_exit_result_code():

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = check_images_changes(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.EXIT


def given_an_empty_structure_it_should_return_an_exit_result_code():

    dvc_diff_with_added_gold_image = {}

    result = check_images_changes(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.EXIT


def given_a_diff_structure_with_changes_it_should_return_an_continue_result_code():

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [
            {"path": "data/000001/52/000001-52.600.2.tif"},
        ],
        "modified": [],
        "renamed": [],
    }

    result = check_images_changes(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.CONTINUE
