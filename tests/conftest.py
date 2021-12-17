# Problem: Pytest do not support namescape packages.
#
# From Pytest docs:
#
# "You can use Python3 namespace packages (PEP420) for your application but pytest will still perform
# test package name discovery based on the presence of __init__.py files."
#
# From: https://docs.pytest.org/en/6.2.x/goodpractices.html#tests-as-part-of-application-code
#
# Solution:
#
# Apply patch to "_pytest.pathlib.resolve_package_path" method to consider all dirs in tests/ namespace packages.
#
# From:
# https://stackoverflow.com/questions/50174130/how-do-i-pytest-a-project-using-pep-420-namespace-packages/50175552#50175552


import pathlib

import _pytest.pathlib
import pytest

resolve_pkg_path_orig = _pytest.pathlib.resolve_package_path

# we consider all dirs in tests/ to be namespace packages
rootdir = pathlib.Path(__file__).parent.resolve()
namespace_pkg_dirs = [str(d) for d in rootdir.iterdir() if d.is_dir()]


# patched method
def resolve_package_path(path):
    # call original lookup
    result = resolve_pkg_path_orig(path)
    if result is not None:
        return result
    # original lookup failed, check if we are subdir of a namespace package
    # if yes, return the namespace package we belong to
    for parent in path.parents:
        if str(parent) in namespace_pkg_dirs:
            return parent
    return None


# apply patch
_pytest.pathlib.resolve_package_path = resolve_package_path

# Fixtures


def get_fixtures_dir():
    """
    It's a helper function to use only in tests.
    It gives you the test folder where we store tests fixtures like: example images, gpg keys, etcetera.
    """
    return pathlib.Path().resolve() / "tests/fixtures"


@pytest.fixture()
def temp_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("test_dir")
    return fn


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
