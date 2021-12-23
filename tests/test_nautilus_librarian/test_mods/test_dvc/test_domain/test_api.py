# pylint: disable=no-member
# Dinamically added members of GIT API Repo object are not detected by pyLint

import os.path
from os import path

import pytest
from git import Repo

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper


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
    DvcApiWrapper.init(temp_dir)
    add_remote_to_dvc(temp_dir, temp_dvc_remote)
    create_test_contents(temp_dir)
    return temp_dir


def push_test_contents(temp_dir):
    repo = Repo(temp_dir)
    repo.add("test.data.dvc")
    repo.push(repo.push(refspec="master:master"))


def test_api_wrapper_initialization(temp_dir):
    DvcApiWrapper.init(temp_dir)
    api = DvcApiWrapper(temp_dir)

    assert isinstance(api, DvcApiWrapper)


def test_dvc_init(temp_dir):
    DvcApiWrapper.init(temp_dir)
    DvcApiWrapper(temp_dir)

    assert path.exists(f"{temp_dir}/.dvc")


def test_add(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")

    assert path.exists(f"{temp_dvc_dir_with_test_content}/test.data.dvc")
    assert path.exists(f"{temp_dvc_dir_with_test_content}/.gitignore")


def test_status(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")

    assert api.status(remote="localremote") == {"test.data": "new"}


def test_push(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")
    api.push()

    assert api.status(remote="localremote") == {}


def test_pull(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    # Add a new file
    api.add("test.data")
    assert path.exists("test.data")

    # Push the file to the remote storage
    api.push()

    # Remove the local file
    remove_test_contents(temp_dvc_dir_with_test_content)
    assert not path.exists(f"{temp_dvc_dir_with_test_content}/test.data")

    # Pull the file from remote
    api.pull()

    # The file should be pulled from remote
    assert path.exists(f"{temp_dvc_dir_with_test_content}/test.data")


def test_list(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")
    api.push()

    expected_list_output = [
        {"isout": False, "isdir": False, "isexec": False, "path": ".dvcignore"},
        {"isout": False, "isdir": False, "isexec": False, "path": ".gitignore"},
        {"isout": True, "isdir": False, "isexec": False, "path": "test.data"},
        {"isout": False, "isdir": False, "isexec": False, "path": "test.data.dvc"},
    ]
    assert api.list(temp_dvc_dir_with_test_content) == expected_list_output
