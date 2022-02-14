# pylint: disable=no-member
# Dinamically added members of GIT API Repo object are not detected by pyLint

import os.path
from os import path

import pytest
from git import Repo
from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.mods.dvc.domain.dvc_command_wrapper import dvc
from nautilus_librarian.mods.dvc.domain.dvc_services_api import DvcServicesApi


def create_librarian_test_contents(temp_dir):
    with open(path.join(temp_dir, "000001-32.600.2.tif"), "w") as file:
        file.write("Image contents")


def remove_librarian_test_contents(temp_dir):
    os.remove(f"{temp_dir}/000001-32.600.2.tif")


@pytest.fixture()
def temp_dvc_dir_with_librarian_test_content(temp_dir, temp_dvc_remote):
    DvcApiWrapper.init(temp_dir)
    dvc(temp_dir).add_local_remote_as_default("localremote", temp_dvc_remote)
    create_librarian_test_contents(temp_dir)
    return temp_dir


def push_test_contents(temp_dir):
    repo = Repo(temp_dir)
    repo.add("000001-32.600.2.tif.dvc")
    repo.push(repo.push(refspec="master:master"))


def test_api_services_initialization(temp_dvc_dir_with_librarian_test_content):
    api = DvcServicesApi(temp_dvc_dir_with_librarian_test_content)
    assert isinstance(api, DvcServicesApi)


def test_diff_when_there_is_no_change(temp_dvc_dir_with_librarian_test_content):
    api = DvcServicesApi(temp_dvc_dir_with_librarian_test_content)

    diff = api.diff("HEAD^", "HEAD")

    assert diff == {}


def test_add(temp_dvc_dir_with_librarian_test_content):
    api = DvcServicesApi(temp_dvc_dir_with_librarian_test_content)

    api.add(f"{temp_dvc_dir_with_librarian_test_content}/000001-32.600.2.tif")

    assert path.exists(f"{temp_dvc_dir_with_librarian_test_content}/000001-32.600.2.tif.dvc")
    assert path.exists(f"{temp_dvc_dir_with_librarian_test_content}/.gitignore")


def test_move(temp_dvc_dir_with_librarian_test_content):
    api = DvcServicesApi(temp_dvc_dir_with_librarian_test_content)

    src_image = f"{temp_dvc_dir_with_librarian_test_content}/000001-32.600.2.tif"
    dst_image = f"{temp_dvc_dir_with_librarian_test_content}/000002-32.600.2.tif"

    api.add(src_image)
    api.move(src_image, dst_image)

    assert path.exists(f"{dst_image}.dvc")
    assert not path.exists(f"{src_image}.dvc")
    assert path.exists(dst_image)
    assert not path.exists(src_image)
    assert path.exists(f"{temp_dvc_dir_with_librarian_test_content}/.gitignore")


def test_remove(temp_dvc_dir_with_librarian_test_content):
    api = DvcServicesApi(temp_dvc_dir_with_librarian_test_content)
    image_path = f"{temp_dvc_dir_with_librarian_test_content}/000001-32.600.2.tif"

    api.add(image_path)

    assert path.exists(f"{image_path}.dvc")

    api.remove(image_path)

    assert not path.exists(f"{image_path}.dvc")


def test_push(temp_dvc_dir_with_librarian_test_content):
    api = DvcServicesApi(temp_dvc_dir_with_librarian_test_content)
    image_path = f"{temp_dvc_dir_with_librarian_test_content}/000001-32.600.2.tif"

    api.add(image_path)
    api.push(image_path)

    dvc_api_wrapper = DvcApiWrapper(temp_dvc_dir_with_librarian_test_content)
    assert dvc_api_wrapper.status(remote="localremote") == {}


def test_pull(temp_dvc_dir_with_librarian_test_content):
    api = DvcServicesApi(temp_dvc_dir_with_librarian_test_content)
    image_path = f"{temp_dvc_dir_with_librarian_test_content}/000001-32.600.2.tif"

    api.add(image_path)
    api.push(image_path)
    remove_librarian_test_contents(temp_dvc_dir_with_librarian_test_content)
    assert not path.exists(image_path)

    api.pull()
    assert path.exists(image_path)


def test_files_to_commit(temp_dvc_dir_with_librarian_test_content):

    api = DvcServicesApi(temp_dvc_dir_with_librarian_test_content)

    filepaths = api.get_files_to_commit("data/000001/42/000001-42.600.2.tif")

    assert filepaths == [
        "data/000001/42/.gitignore",
        "data/000001/42/000001-42.600.2.tif.dvc",
    ]
