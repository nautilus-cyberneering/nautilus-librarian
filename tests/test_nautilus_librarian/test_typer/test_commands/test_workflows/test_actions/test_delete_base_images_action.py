# jscpd:ignore-start
from os import path

from test_nautilus_librarian.test_typer.test_commands.test_workflows.test_actions.test_rename_base_images_action import (  # noqa: E501
    copy_base_image_to_destination,
)
from test_nautilus_librarian.test_typer.test_commands.test_workflows.test_gold_images_processing import (
    create_initial_state,
)
from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.console.domain.utils import execute_shell_command
from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.delete_base_images_action import (
    delete_base_images_action,
)

# jscpd:ignore-end


def given_a_diff_structure_with_deleted_gold_image_it_should_delete_base_images(
    sample_gold_image_absolute_path,
    sample_base_image_absolute_path,
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    temp_gpg_home_dir,
    git_user,
):

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [
            {"path": sample_gold_image_absolute_path},
        ],
        "modified": [],
        "renamed": [],
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
        dvc add data/000001/52/000001-52.600.2.tif
    """,
        cwd=temp_git_dir,
    )

    assert path.exists(f"{temp_git_dir}/data/000001/52/000001-52.600.2.tif.dvc")

    result = delete_base_images_action(
        compact_json(dvc_diff_with_added_gold_image), temp_git_dir
    )

    assert result.code == ResultCode.CONTINUE
    assert not path.exists(f"{temp_git_dir}/data/000001/52/000001-52.600.2.tif.dvc")
    assert result.contains_text("successfully deleted")
