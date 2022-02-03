from os import makedirs, path
from shutil import copy

from test_nautilus_librarian.test_typer.test_commands.test_workflows.test_gold_images_processing import (
    create_initial_state,
)
from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.console.domain.utils import execute_shell_command
from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.rename_base_images_action import (
    rename_base_images,
)


def copy_base_image_to_destination(sample_base_image_absolute_path, destination_dir):
    makedirs(f"{destination_dir}/data/000001/42/", exist_ok=True)
    copy(
        sample_base_image_absolute_path,
        f"{destination_dir}/data/000001/42/000001-42.600.2.tif",
    )


def given_a_diff_structure_with_renamed_gold_image_it_should_rename_base_images(
    sample_gold_image_absolute_path,
    sample_base_image_absolute_path,
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    temp_gpg_home_dir,
    git_user,
):

    dvc_diff_with_renamed_gold_image = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [
            {
                "path": {
                    "old": "data/000001/32/000001-32.600.2.tif",
                    "new": "data/000001/32/000002-32.600.2.tif",
                }
            },
        ],
    }

    create_initial_state(
        temp_git_dir,
        temp_dvc_local_remote_storage_dir,
        sample_gold_image_absolute_path,
        temp_gpg_home_dir,
        git_user,
    )
    copy_base_image_to_destination(sample_base_image_absolute_path, temp_git_dir)

    execute_shell_command(
        """
        ls -la
        dvc add data/000001/42/000001-42.600.2.tif
    """,
        cwd=temp_git_dir,
    )

    result = rename_base_images(
        compact_json(dvc_diff_with_renamed_gold_image), temp_git_dir
    )

    print(f"{result.messages[0]}")
    assert result.code == ResultCode.CONTINUE
    assert path.exists(f"{temp_git_dir}/data/000002/42/000002-42.600.2.tif")
    assert result.contains_text("successfully renamed to")
