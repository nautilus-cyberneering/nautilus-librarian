from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.check_images_changes_action import (
    check_images_changes_action,
)


def given_an_empty_dvc_diff_it_should_exit():

    dvc_diff_with_added_gold_image = {}

    result = check_images_changes_action(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.EXIT


def given_a_diff_structure_with_no_changes_it_should_exit():

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = check_images_changes_action(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.EXIT


def given_a_diff_structure_with_added_files_it_should_continue():

    dvc_diff_with_added_gold_image = {
        "added": [
            {"path": "data/000001/52/000001-52.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = check_images_changes_action(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.CONTINUE


def given_a_diff_structure_with_deleted_files_it_should_continue():

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [
            {"path": "data/000001/52/000001-52.600.2.tif"},
        ],
        "modified": [],
        "renamed": [],
    }

    result = check_images_changes_action(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.CONTINUE


def given_a_diff_structure_with_modified_files_it_should_continue():

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [],
        "modified": [
            {"path": "data/000001/52/000001-52.600.2.tif"},
        ],
        "renamed": [],
    }

    result = check_images_changes_action(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.CONTINUE


def given_a_diff_structure_with_renamed_files_it_should_continue():

    dvc_diff_with_added_gold_image = {
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

    result = check_images_changes_action(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.CONTINUE
