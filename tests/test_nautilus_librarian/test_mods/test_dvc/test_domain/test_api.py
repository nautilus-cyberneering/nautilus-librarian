# pylint: disable=no-member
# Dinamically added members of GIT API Repo object are not detected by pyLint

import os.path
from os import path

import pytest
from git import Repo

import nautilus_librarian.mods.dvc.domain.api as DvcApi
from nautilus_librarian.mods.console.domain.utils import (
    change_current_working_directory,
    execute_console_command,
)


@pytest.fixture()
def temp_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("test_dir")
    return fn


@pytest.fixture()
def temp_dvc_remote(tmp_path_factory):
    fn = tmp_path_factory.mktemp("test_dvc_remote_dir")
    return fn


def create_test_contents(temp_dir):
    with open(path.join(temp_dir, "test.data"), "w") as file:
        file.write("lorem ipsum")


def remove_test_contents(temp_dir):
    os.remove(f"{temp_dir}/test.data")


def add_remote_to_dvc(dvc_dir, remote_temp_dir):
    execute_console_command(
        f"dvc remote add -d localremote {remote_temp_dir}", cwd=dvc_dir
    )


@pytest.fixture()
def temp_dvc_dir_with_test_content(temp_dir, temp_dvc_remote):
    Repo.init(temp_dir)
    DvcApi.init(temp_dir)
    add_remote_to_dvc(temp_dir, temp_dvc_remote)
    create_test_contents(temp_dir)
    return temp_dir


def push_test_contents(temp_dir):
    repo = Repo(temp_dir)
    repo.add("test.data.dvc")
    repo.push(repo.push(refspec="master:master"))


def test_dvc_init(temp_dir):
    Repo.init(temp_dir)
    DvcApi.init(temp_dir, no_scm=False)

    assert path.exists(f"{temp_dir}/.dvc")


def test_initializing_dvc_without_git(temp_dir):
    """
    https://dvc.org/doc/command-reference/init#initializing-dvc-without-git
    """
    DvcApi.init(temp_dir, no_scm=True)

    assert path.exists(f"{temp_dir}/.dvc")


def test_add(temp_dvc_dir_with_test_content):
    change_current_working_directory(temp_dvc_dir_with_test_content)
    DvcApi.add(temp_dvc_dir_with_test_content, "test.data")

    assert path.exists("test.data.dvc")
    assert path.exists(".gitignore")


def test_status(temp_dvc_dir_with_test_content):
    change_current_working_directory(temp_dvc_dir_with_test_content)

    DvcApi.add(temp_dvc_dir_with_test_content, "test.data")

    assert DvcApi.status(temp_dvc_dir_with_test_content, remote="localremote") == {
        "test.data": "new"
    }


def test_push(temp_dvc_dir_with_test_content):
    change_current_working_directory(temp_dvc_dir_with_test_content)

    DvcApi.add(temp_dvc_dir_with_test_content, "test.data")
    DvcApi.push(temp_dvc_dir_with_test_content)

    assert DvcApi.status(temp_dvc_dir_with_test_content, remote="localremote") == {}


def test_pull(temp_dvc_dir_with_test_content):
    change_current_working_directory(temp_dvc_dir_with_test_content)

    # Add a new file
    DvcApi.add(temp_dvc_dir_with_test_content, "test.data")
    assert path.exists("test.data")

    # Push the file to the remote storage
    DvcApi.push(temp_dvc_dir_with_test_content)

    # Remove the local file
    remove_test_contents(temp_dvc_dir_with_test_content)
    assert not path.exists("test.data")

    # Pull the file from remote
    DvcApi.pull(temp_dvc_dir_with_test_content)

    # The file should be pulled from remote
    assert path.exists(f"{temp_dvc_dir_with_test_content}/test.data")


def test_list(temp_dvc_dir_with_test_content):
    change_current_working_directory(temp_dvc_dir_with_test_content)

    DvcApi.add(temp_dvc_dir_with_test_content, "test.data")
    DvcApi.push(temp_dvc_dir_with_test_content)

    expected_list_output = [
        {"isout": False, "isdir": False, "isexec": False, "path": ".dvcignore"},
        {"isout": False, "isdir": False, "isexec": False, "path": ".gitignore"},
        {"isout": True, "isdir": False, "isexec": False, "path": "test.data"},
        {"isout": False, "isdir": False, "isexec": False, "path": "test.data.dvc"},
    ]
    assert DvcApi.list(temp_dvc_dir_with_test_content) == expected_list_output
