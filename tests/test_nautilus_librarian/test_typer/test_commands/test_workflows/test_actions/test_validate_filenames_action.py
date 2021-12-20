from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.validate_filenames import (
    validate_filenames,
)


def given_a_dvc_diff_object_it_should_validate_the_filename_of_the_new_media_files(
    temp_git_dir, temp_dvc_local_remote_storage_dir, sample_base_image_absolute_path
):
    dvc_diff_with_added_gold_image = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = validate_filenames(compact_json(dvc_diff_with_added_gold_image))

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text("000001-32.600.2.tif ✓")
