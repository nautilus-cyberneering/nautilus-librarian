import pytest


@pytest.fixture()
def temp_dvc_local_remote_storage_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("storage")
    return fn


@pytest.fixture()
def temp_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("test_dir")
    return fn


@pytest.fixture()
def temp_dvc_remote(tmp_path_factory):
    fn = tmp_path_factory.mktemp("test_dvc_remote_dir")
    return fn
