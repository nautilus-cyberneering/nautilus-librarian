from shutil import copytree

from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.rename_base_images_action import (
    rename_base_images,
)


def copy_fixtures_to_tmp_path(fixtures_dir, temp_path):
    copytree(fixtures_dir, temp_path)


def given_a_diff_structure_with_renamed_gold_image_it_should_rename_base_images(
    sample_gold_image_absolute_path,
    renamed_sample_gold_image_absolute_path,
    tmp_path_factory,
    workflows_fixtures_dir,
):

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [
            {
                "path": {
                    "old": sample_gold_image_absolute_path,
                    "new": renamed_sample_gold_image_absolute_path,
                }
            },
        ],
    }

    temp_path = tmp_path_factory.mktemp("repo")
    copy_fixtures_to_tmp_path(
        f"{workflows_fixtures_dir}/data", f"{temp_path}/test_repo/data"
    )

    result = rename_base_images(
        compact_json(dvc_diff_with_added_gold_image), f"{temp_path}/test_repo"
    )

    assert result.code == ResultCode.CONTINUE
    print(result.messages)
    assert result.contains_text("successfully renamed to")
