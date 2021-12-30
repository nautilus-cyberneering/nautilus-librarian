
import os
from shutil import copy

from typer.testing import CliRunner

from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.main import app
from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.namecodes.domain.filename import Filename

runner = CliRunner()


def assert_expected_output(output, expected_output):
    """
    It removes the indentation from the expected output because the real output does not have indentation.
    """
    lines = expected_output.splitlines()

    # Remove first line break
    lines.pop(0)

    # Remove indentation
    lines_without_indent = [line.strip() for line in lines]

    # Join the string back
    expected_output_without_indent = "\n".join(lines_without_indent)

    assert output == expected_output_without_indent


def create_initial_state(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    sample_base_image_absolute_path,
    temp_gpg_home_dir,
    git_user,
    remote_name="localremote",
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
        dvc remote add -d {remote_name} {temp_dvc_local_remote_storage_dir}
        git add -A
        GNUPGHOME={temp_gpg_home_dir} git commit -S --gpg-sign={git_user.signingkey} -m "dvc add remote" --author="{git_user.name} <{git_user.email}>" # noqa
        mkdir -p {sample_base_image_dir}
    """,
        cwd=temp_git_dir,
    )

    # Copy the Base sample Base image to its folder
    copy(sample_base_image_absolute_path, f"{temp_git_dir}/{sample_base_image_dir}")


def add_gold_image(git_dir, sample_gold_image_absolute_path, gpg_home_dir, git_user):
    # Copy the Base sample Base image to its folder
    filename = Filename(sample_gold_image_absolute_path)
    sample_gold_image_dir = file_locator(filename)
    os.mkdir(f"{git_dir}/{sample_gold_image_dir}")
    copy(sample_gold_image_absolute_path, f"{git_dir}/{sample_gold_image_dir}")

    # Add the newly copied file to the DVC cache
    execute_console_command(
        f"""
        dvc add data/000001/32/000001-32.600.2.tif
        dvc push
        git add data/000001/32/000001-32.600.2.tif.dvc data/000001/32/.gitignore
        GNUPGHOME={gpg_home_dir} git commit -S --gpg-sign={git_user.signingkey} -m "feat: new gold image: 000001-32.600.2.tif" --author="{git_user.name} <{git_user.email}>" # noqa
    """,
        cwd=git_dir,
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
            "NL_GIT_REPO_DIR": str(temp_git_dir),
            "NL_GIT_USER_NAME": git_user.name,
            "NL_GIT_USER_EMAIL": git_user.email,
            "NL_GIT_USER_SIGNINGKEY": git_user.signingkey,
            "GNUPGHOME": str(temp_gpg_home_dir),
        },
    )
    assert result.exit_code == 0
    assert "No Gold image changes found" in result.stdout


def copy_media_file_to_its_folder(src_media_file_path, git_dir):
    """
    Given a library file in a source location, it copies it to the git repo in the right folder.
    """

    media_file_relative_dir = file_locator(Filename(src_media_file_path))

    dest_media_file_dir = f"{git_dir}/{media_file_relative_dir}"

    # Create dest dir if it does not exist
    os.makedirs(dest_media_file_dir, exist_ok=True)

    copy(src_media_file_path, dest_media_file_dir)


def test_gold_images_processing_workflow_command(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    sample_gold_image_absolute_path,
    sample_base_image_absolute_path,
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

    add_gold_image(
        temp_git_dir, sample_gold_image_absolute_path, temp_gpg_home_dir, git_user
    )
    copy_media_file_to_its_folder(sample_gold_image_absolute_path, temp_git_dir)

    # Add the new Gold image

    result = runner.invoke(
        app,
        ["gold-images-processing"],
        env={
            "NL_GIT_REPO_DIR": str(temp_git_dir),
            "NL_GIT_USER_NAME": git_user.name,
            "NL_GIT_USER_EMAIL": git_user.email,
            "NL_GIT_USER_SIGNINGKEY": git_user.signingkey,
            "NL_CURRENT_REF": "HEAD",
            "NL_PREVIOUS_REF": "HEAD^",
            "GNUPGHOME": str(temp_gpg_home_dir),
        },
    )

    assert result.exit_code == 0

    expected_output = """
    000001-32.600.2.tif ✓
    data/000001/32/000001-32.600.2.tif ✓
    ✓ data/000001/32/000001-32.600.2.tif pulled from dvc storage
    New Gold image found: 000001-32.600.2.tif -> Base image: data/000001/42/000001-42.600.2.tif ✓
    """

    assert_expected_output(result.stdout, expected_output)
