from os import mkdir
from shutil import copy

from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.main import app
from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from typer.testing import CliRunner

runner = CliRunner()


def create_initial_state(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    sample_base_image_absolute_path,
    temp_gpg_home_dir,
    git_user,
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
    sample_base_image_dir = file_locator(Filename(sample_base_image_absolute_path))

    execute_console_command(
        f"""
        git init
        dvc init
        git add -A
        GNUPGHOME={temp_gpg_home_dir} git commit -S --gpg-sign={git_user.signingkey} -m "dvc init" --author="{git_user.name} <{git_user.email}>" # noqa
        dvc remote add -d localremote {temp_dvc_local_remote_storage_dir}
        git add -A
        GNUPGHOME={temp_gpg_home_dir} git commit -S --gpg-sign={git_user.signingkey} -m "dvc add remote" --author="{git_user.name} <{git_user.email}>" # noqa
        mkdir -p {sample_base_image_dir}
    """,
        cwd=temp_git_dir,
    )

    # Copy the Base sample Base image to its folder
    copy(sample_base_image_absolute_path, f"{temp_git_dir}/{sample_base_image_dir}")


def add_gold_image(temp_git_dir, sample_gold_image_absolute_path):
    # Copy the Base sample Base image to its folder
    filename = Filename(sample_gold_image_absolute_path)
    sample_gold_image_dir = file_locator(filename)
    mkdir(f"{temp_git_dir}/{sample_gold_image_dir}")
    copy(sample_gold_image_absolute_path, f"{temp_git_dir}/{sample_gold_image_dir}")

    # Add the newly copied file to the DVC cache
    execute_console_command(
        f"dvc add {sample_gold_image_dir}/{filename}",
        cwd=temp_git_dir,
    )


def it_should_show_a_message_if_there_is_not_any_change_in_gold_images(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    sample_base_image_absolute_path,
    temp_gpg_home_dir,
    git_user,
):
    create_initial_state(
        temp_git_dir,
        temp_dvc_local_remote_storage_dir,
        sample_base_image_absolute_path,
        temp_gpg_home_dir,
        git_user,
    )

    result = runner.invoke(
        app,
        ["gold-images-processing"],
        env={
            "INPUT_GIT_REPO_DIR": str(temp_git_dir),
            "INPUT_GIT_USER_NAME": git_user.name,
            "INPUT_GIT_USER_EMAIL": git_user.email,
            "INPUT_GIT_USER_SIGNINGKEY": git_user.signingkey,
            "GNUPGHOME": str(temp_gpg_home_dir),
        },
    )

    assert result.exit_code == 0
    assert "No Gold image changes found" in result.stdout


def test_gold_images_processing_workflow_command(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    sample_base_image_absolute_path,
    sample_gold_image_absolute_path,
    temp_gpg_home_dir,
    git_user,
):
    """
    This is the acceptance test for the whole command and for the happy path.
    Every step in the workflow has its own independent unit test.
    """
    create_initial_state(
        temp_git_dir,
        temp_dvc_local_remote_storage_dir,
        sample_base_image_absolute_path,
        temp_gpg_home_dir,
        git_user,
    )

    add_gold_image(temp_git_dir, sample_gold_image_absolute_path)
    result = runner.invoke(
        app,
        ["gold-images-processing"],
        env={
            "INPUT_GIT_REPO_DIR": str(temp_git_dir),
            "INPUT_GIT_USER_NAME": git_user.name,
            "INPUT_GIT_USER_EMAIL": git_user.email,
            "INPUT_GIT_USER_SIGNINGKEY": git_user.signingkey,
            "GNUPGHOME": str(temp_gpg_home_dir),
        },
    )

    assert result.exit_code == 0
    assert (
        "000001-32.600.2.tif ✓\nNew Gold image found: 000001-32.600.2.tif -> Base image: data/000001/42/000001-42.600.2.tif ✓ \n"  # noqa
        in result.stdout
    )
