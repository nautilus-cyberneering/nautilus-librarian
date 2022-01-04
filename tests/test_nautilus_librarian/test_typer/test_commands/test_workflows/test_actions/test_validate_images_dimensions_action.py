from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.validate_images_dimensions_action import (
    validate_images_dimensions,
)


def given_a_diff_structure_and_size_limits_it_should_validate_new_image_dimensions(sample_gold_image_absolute_path):

    dvc_diff_with_added_gold_image = {
        "added": [
            {"path": sample_gold_image_absolute_path},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = validate_images_dimensions(compact_json(dvc_diff_with_added_gold_image), 512, 4096)

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text("Dimensions of "+sample_gold_image_absolute_path+" are 1740 x 1160 ✓")


def given_a_diff_structure_and_size_limits_it_should_validate_modified_image_dimensions(sample_gold_image_absolute_path):

    dvc_diff_with_modified_image = {
        "added": [],
        "deleted": [],
        "modified": [
            {"path": sample_gold_image_absolute_path},
        ],
        "renamed": [],
    }

    result = validate_images_dimensions(compact_json(dvc_diff_with_modified_image), 512, 4096)

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text("Dimensions of "+sample_gold_image_absolute_path+" are 1740 x 1160 ✓")


def given_a_diff_structure_and_size_limits_it_should_validate_renamed_image_dimensions(sample_gold_image_absolute_path):

    dvc_diff_with_renamed_image = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [
            {"path": sample_gold_image_absolute_path},
        ],
    }

    result = validate_images_dimensions(compact_json(dvc_diff_with_renamed_image), 512, 4096)

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text("Dimensions of "+sample_gold_image_absolute_path+" are 1740 x 1160 ✓")


def given_a_diff_structure_and_size_limits_it_should_not_validate_new_image_dimensions(sample_gold_image_absolute_path):

    dvc_diff_with_added_image = {
        "added": [
            {"path": sample_gold_image_absolute_path},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = validate_images_dimensions(compact_json(dvc_diff_with_added_image), 8, 16)

    expected_message = f"✗ Dimensions of {sample_gold_image_absolute_path} are not correct: File dimensions (1740 x 1160) bigger than maximum size of 16"

    assert result.code == ResultCode.ABORT
    assert expected_message.strip() == result.last_message_text()
