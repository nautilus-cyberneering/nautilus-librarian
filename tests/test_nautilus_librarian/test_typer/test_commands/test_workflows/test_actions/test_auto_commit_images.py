import os

from git.repo.base import Repo
from test_nautilus_librarian.test_typer.test_commands.test_workflows.test_actions.test_rename_base_images_action import (  # noqa: E501
    copy_base_image_to_destination,
)
from test_nautilus_librarian.test_typer.test_commands.test_workflows.test_gold_images_processing import (
    create_initial_state,
)
from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.dvc.domain.dvc_command_wrapper import dvc
from nautilus_librarian.mods.git.domain.git_command_wrapper import git
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.auto_commit_base_images import (
    auto_commit_base_images,
    calculate_the_corresponding_base_image_from_gold_image,
    files_to_commit,
    get_new_gold_images_filenames_from_dvc_diff,
)


def test_get_new_gold_images_from_dvc_diff():

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/000001/42/000001-42.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = get_new_gold_images_filenames_from_dvc_diff(compact_json(dvc_diff))

    assert result == [Filename("data/000001/32/000001-32.600.2.tif")]


def test_files_to_commit():
    filepaths = files_to_commit("data/000001/42/000001-42.600.2.tif")

    assert filepaths == [
        "data/000001/42/.gitignore",
        "data/000001/42/000001-42.600.2.tif.dvc",
    ]


def test_calculate_the_corresponding_base_image_from_gold_image():
    git_repo_dir = "/home/repo"
    gold_image = Filename("000001-32.600.2.tif")

    base_image_path = calculate_the_corresponding_base_image_from_gold_image(
        git_repo_dir, gold_image
    )

    assert base_image_path == (
        "data/000001/42/000001-42.600.2.tif",  # relative path
        "/home/repo/data/000001/42/000001-42.600.2.tif",  # absolute path
    )

def remove_base_image_dvc_files(temp_git_dir):
    os.remove(f"{temp_git_dir}/data/000001/42/000001-42.600.2.tif.dvc")
    os.remove(f"{temp_git_dir}/data/000001/42/.gitignore")


def commit_added_base_images(temp_git_dir, temp_gpg_home_dir, git_user):

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    return auto_commit_base_images(
        compact_json(dvc_diff), str(temp_git_dir), str(temp_gpg_home_dir), git_user
    )


def given_a_dvc_diff_object_with_a_new_gold_image_it_should_commit_the_added_base_image_to_dvc(
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

    result = commit_added_base_images(temp_git_dir, temp_gpg_home_dir, git_user)

    # Assert command runned successfully
    assert result.code == ResultCode.CONTINUE

    # Assert Base image was created
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/000001-42.600.2.tif")

    # DVC Asserts

    # Assert dvc files were created
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/000001-42.600.2.tif.dvc")
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/.gitignore")

    # Assert Base image was pushed to local "remote" storage
    dvc_status_output_json = dvc(temp_git_dir).status_remote("localremote")
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
    assert commit.committer.name == git_user.name
    assert commit.committer.email == git_user.email

    # Assert the commit was signed with the right signing key
    assert (
        git(temp_git_dir).get_commit_signing_key(commit.hexsha) == git_user.signingkey
    )


def given_a_dvc_diff_object_with_a_gold_image_deleton_it_should_commit_the_base_image_deletion_to_git(
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

    commit_added_base_images(temp_git_dir, temp_gpg_home_dir, git_user)

    remove_base_image_dvc_files(temp_git_dir)

    dvc_diff = {
        "added": [],
        "deleted": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "modified": [],
        "renamed": [],
    }
    
    result = auto_commit_base_images(
        compact_json(dvc_diff), str(temp_git_dir), str(temp_gpg_home_dir), git_user
    )

    # Assert command runned successfully
    assert result.code == ResultCode.CONTINUE

    # Git commit Asserts

    # Assert Base commit was created
    repo = Repo(temp_git_dir)
    commit = repo.commit(repo.heads[0].commit)  # latest commit on the branch

    # Assert the commit has the right message
    assert commit.summary == "feat: deleted base image: 000001-42.600.2.tif"

    # Assert the commit contains the right files
    expected_commit_stats_files = {
        "data/000001/42/.gitignore": {"insertions": 0, "deletions": 1, "lines": 1},
        "data/000001/42/000001-42.600.2.tif.dvc": {
            "insertions": 0,
            "deletions": 4,
            "lines": 4,
        },
    }
    assert commit.stats.files == expected_commit_stats_files

    # Assert the commit was created by the right user
    assert commit.committer.name == git_user.name
    assert commit.committer.email == git_user.email

    # Assert the commit was signed with the right signing key
    assert (
        git(temp_git_dir).get_commit_signing_key(commit.hexsha) == git_user.signingkey
    )
