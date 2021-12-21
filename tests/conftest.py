import pathlib
from shutil import copy

import _pytest.pathlib
import pytest

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.gpg.domain.utils import (
    import_gpg_private_key,
    preset_passphrase,
)

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


@pytest.fixture(scope="session")
def temp_gpg_home_dir(tmp_path_factory):
    # New tmp dir for GPG homedir
    gnupghome = tmp_path_factory.mktemp("gnupg")

    # Apply GPG conf
    gpg_agent_conf_template = f"{get_fixtures_dir()}/gpg/gpg-agent.conf"
    copy(gpg_agent_conf_template, gnupghome)
    execute_console_command(
        f"""
        gpg-connect-agent --homedir {gnupghome} RELOADAGENT /bye
    """
    )

    # Read the GPG private key used for testing
    # secretlint-disable
    committer_gpg_private_key_path = (
        f"{get_fixtures_dir()}/gpg/committer_private_key.pgp"
    )
    gpg_private_key = "-----BEGIN PGP PRIVATE KEY BLOCK-----\n\n"
    with open(committer_gpg_private_key_path, "r") as f:
        gpg_private_key += f.read()
    gpg_private_key += "\n\n-----END PGP PRIVATE KEY BLOCK-----\n"
    # secretlint-enable

    passphrase = "123456"  # nosec

    # Import the GPG key in the temp GPG homedir
    keygrip, signingkey, user_name, user_email = import_gpg_private_key(
        gpg_private_key, passphrase=passphrase, gnupghome=str(gnupghome)
    )

    # Debug: check if the GPG was imported correctly
    execute_console_command(
        f"gpg --homedir {gnupghome} -k", cwd=gnupghome, print_output=True
    )

    # The keygrip of the subkey we use to sign
    # TODO: use a test function to get the git test user attributes: name, email, signingkey
    keygrip_for_key_3F39AA1432CA6AD7 = "00CB9308AE0B6DE018C5ADBAB29BA7899D6062BE"

    # Preset passphrase to avoid entering it manually while running tests
    preset_passphrase(keygrip_for_key_3F39AA1432CA6AD7, passphrase, gnupghome)

    return gnupghome
