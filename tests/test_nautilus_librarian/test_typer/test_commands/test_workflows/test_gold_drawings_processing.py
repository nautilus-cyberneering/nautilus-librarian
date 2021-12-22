import json
import os
from shutil import copy

from git.repo.base import Repo
from test_nautilus_librarian.utils import compact_json
from typer.testing import CliRunner

from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.main import app
from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.git.domain.commit import get_commit_signing_key
from nautilus_librarian.mods.namecodes.domain.filename import Filename

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


def it_should_show_a_message_if_there_is_not_any_change_in_gold_images():
    result = runner.invoke(app, ["gold-drawings-processing"])

    assert result.exit_code == 0
    assert "No Gold image changes found" in result.stdout


def given_a_dvc_diff_object_with_a_new_gold_image_it_should_commit_the_added_base_image_to_dvc(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    sample_base_image_absolute_path,
    temp_gpg_home_dir,
    test_git_user,
):
    create_initial_state(
        temp_git_dir,
        temp_dvc_local_remote_storage_dir,
        sample_base_image_absolute_path,
        temp_gpg_home_dir,
        test_git_user,
    )

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    # Execute the workflow
    result = runner.invoke(
        app,
        ["gold-drawings-processing", compact_json(dvc_diff)],
        env={
            "INPUT_GIT_REPO_DIR": str(temp_git_dir),
            "INPUT_GIT_USER_NAME": test_git_user.name,
            "INPUT_GIT_USER_EMAIL": test_git_user.email,
            "INPUT_GIT_USER_SIGNINGKEY": test_git_user.signingkey,
            "GNUPGHOME": str(temp_gpg_home_dir),
        },
    )

    # Assert command runned successfully
    assert result.exit_code == 0

    # Assert Base image was created
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/000001-42.600.2.tif")

    # DVC Asserts

    # Assert dvc files were created
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/000001-42.600.2.tif.dvc")
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/.gitignore")

    # Assert Base image was pushed to local "remote" storage
    dvc_status_output = execute_console_command(
        "dvc status --show-json --cloud --remote=localremote", cwd=temp_git_dir
    )
    dvc_status_output_json = json.loads(dvc_status_output)
    expected_status_new = {"data/000001/42/000001-42.600.2.tif": "new"}
    expected_status_empty = {}
    assert (
        expected_status_new == dvc_status_output_json
        or expected_status_empty == dvc_status_output_json
    )

    # Git commit Asserts

    # Assert Base commit was created
    repo = Repo(temp_git_dir)
    commit = repo.commit(repo.heads[0].commit)  # latest commit on the branch

    # Assert the commit has the right message
    assert commit.summary == "feat: new base image: 000001-42.600.2.tif"

    # Assert the commit contains the right files
    expected_commit_stats_files = {
        "data/000001/42/.gitignore": {"insertions": 1, "deletions": 0, "lines": 1},
        "data/000001/42/000001-42.600.2.tif.dvc": {
            "insertions": 4,
            "deletions": 0,
            "lines": 4,
        },
    }
    assert commit.stats.files == expected_commit_stats_files

    # Assert the commit was created by the right user
    assert commit.committer.name == test_git_user.name
    assert commit.committer.email == test_git_user.email

    # Assert the commit was signed with the right signing key
    assert (
        get_commit_signing_key(commit.hexsha, cwd=temp_git_dir)
        == test_git_user.signingkey
    )
