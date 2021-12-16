import json
from shutil import copy

import pytest
from test_nautilus_librarian.utils import execute_console_command, get_fixtures_dir
from typer.testing import CliRunner

from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.main import app
from nautilus_librarian.mods.console.utils import (
    change_current_working_directory,
    get_current_working_directory,
)
from nautilus_librarian.mods.namecodes.domain.filename import Filename

runner = CliRunner()


@pytest.fixture()
def temp_git_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("repo")
    return fn


@pytest.fixture()
def temp_dvc_local_remote_storage_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("storage")
    return fn


@pytest.fixture(scope="session")
def sample_base_image_absolute_path():
    fixtures_dir = get_fixtures_dir()
    base_image_path = f"{fixtures_dir}/000001-42.600.2.tif"
    return base_image_path


def given_a_dvc_diff_object_with_a_new_gold_image_it_should_commit_the_add_the_base_image_to_dvc(
    temp_git_dir, temp_dvc_local_remote_storage_dir, sample_base_image_absolute_path
):

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    """
    'pytest -s' to disable capturing output

    Arrange:
        1. Create a temp dir
        2. Initialize a temp git repo
        3. Initialize dvc in the git repo
        4. Create a "local" remote storage:
            https://dvc.org/doc/command-reference/remote#example-add-a-default-local-remote
        5. Create a Base image

    TODO:
    Act:
        1. Invoke the "gold-drawings-processing" command

    Assert:
        1. The Base image was uploaded to the "remote" dvc local storage
        2. A new signed commit was created on the current branch, containing the dvc pointer and .gitignore file
    """

    tests_working_dir = get_current_working_directory()
    change_current_working_directory(temp_git_dir)

    sample_base_image_dir = file_locator(Filename(sample_base_image_absolute_path))

    # Prerare new empty repo with a local "remote" storage
    # https://dvc.org/doc/command-reference/remote#example-add-a-default-local-remote
    execute_console_command(
        f"""
        pwd
        git init
        dvc init
        dvc remote add -d localremote {temp_dvc_local_remote_storage_dir}
    """
    )

    # Create folder for sample Base image
    execute_console_command(
        f"""
        mkdir -p {sample_base_image_dir}
    """
    )

    # Copy the Base sample Base image to its folder
    copy(sample_base_image_absolute_path, f"{sample_base_image_dir}")

    # Execute the workflow
    result = runner.invoke(
        app,
        ["gold-drawings-processing", json.dumps(dvc_diff, separators=(",", ":"))],
        env=[["INPUT_GIT_REPO_DIR", str(temp_git_dir)]],
    )

    git_status_output = execute_console_command("git status")

    change_current_working_directory(tests_working_dir)

    assert result.exit_code == 0
    assert "No commits yet" in git_status_output
    assert "000001-32.600.2.tif ✓\n" in result.stdout
