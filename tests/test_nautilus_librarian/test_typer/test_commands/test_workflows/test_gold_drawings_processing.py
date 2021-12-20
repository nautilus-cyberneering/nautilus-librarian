from shutil import copy

from typer.testing import CliRunner

from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.main import app
from nautilus_librarian.mods.console.domain.utils import (
    change_current_working_directory,
    execute_console_command,
    get_current_working_directory,
)
from nautilus_librarian.mods.namecodes.domain.filename import Filename

runner = CliRunner()


def create_initial_state(
    temp_git_dir, temp_dvc_local_remote_storage_dir, sample_base_image_absolute_path
):
    """
    Helper function to create the initial state needed to test the workflow.

    1. Create a temp dir
    2. Initialize a git repo in the temp dir
    3. Initialize a dvc repo in the git repo
    4. Create a "local" remote storage with dvc:
        https://dvc.org/doc/command-reference/remote#example-add-a-default-local-remote
    5. Add a example Base image from fixtures dir
    """

    tests_working_dir = get_current_working_directory()
    change_current_working_directory(temp_git_dir)

    sample_base_image_dir = file_locator(Filename(sample_base_image_absolute_path))

    execute_console_command(
        f"""
        git init
        dvc init
        git add -A
        git commit -m "dvc init"
        dvc remote add -d localremote {temp_dvc_local_remote_storage_dir}
        git add -A
        git commit -m "dvc add remote"
        mkdir -p {sample_base_image_dir}
    """
    )

    # Copy the Base sample Base image to its folder
    copy(sample_base_image_absolute_path, f"{sample_base_image_dir}")

    change_current_working_directory(tests_working_dir)


def it_should_show_a_message_if_there_is_not_any_change_in_gold_images():
    result = runner.invoke(app, ["gold-drawings-processing"])

    assert result.exit_code == 0
    assert "No Gold image changes found" in result.stdout
