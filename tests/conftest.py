import os
import pathlib
from pathlib import Path
from shutil import copy

import _pytest.pathlib
import pytest

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.git.domain.git_user import GitUser
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


@pytest.fixture(scope="session")
def fixtures_dir():
    """
    It's a helper function to use only in tests.
    It gives you the test folder where we store tests fixtures like: example images, gpg keys, etcetera.
    """
    current_file_dir = os.path.dirname(Path(__file__).resolve())
    return f"{current_file_dir}/fixtures"


@pytest.fixture(scope="session")
def gpg_key_info(fixtures_dir):
    """
    The GPG key used to sign the commits in tests:

    pub   rsa4096 2021-11-19 [C]
          8896 6A5B 8C01 BD04 F3DA  4404 2730 4EDD 6079 B81C
          Keygrip = 449972AC9FF11BCABEED8A7AE834C4349CC4DBFF
    uid           [ultimate] A committer <committer@example.com>
    sub   rsa4096 2021-11-19 [E]
          B1D4 A248 3D1D 2A02 416B  E077 5B6B DD35 BEDF BF6F
          Keygrip = 97D36F5B8F5BECDA8A1923FC00D11C7C438584F9
    sub   rsa4096 2021-11-26 [S]
          BD98 B3F4 2545 FF93 EFF5  5F7F 3F39 AA14 32CA 6AD7
          Keygrip = 00CB9308AE0B6DE018C5ADBAB29BA7899D6062BE

    We use the subkey with sign [S] capability (3F39 AA14 32CA 6AD7).
    """

    # Read the GPG private key used for testing from a file.
    # The file does not contain the header and footer.
    # secretlint-disable
    committer_gpg_private_key_path = f"{fixtures_dir}/gpg/committer_private_key.pgp"
    gpg_private_key = "-----BEGIN PGP PRIVATE KEY BLOCK-----\n\n"
    with open(committer_gpg_private_key_path, "r") as f:
        gpg_private_key += f.read()
    gpg_private_key += "\n\n-----END PGP PRIVATE KEY BLOCK-----\n"
    # secretlint-enable

    return {
        "long_key": "3F39AA1432CA6AD7",
        "keygrip": "00CB9308AE0B6DE018C5ADBAB29BA7899D6062BE",
        "passphrase": "123456",
        "private_key": gpg_private_key,
    }


@pytest.fixture(scope="session")
def git_user(gpg_key_info):
    """
    The test committer used to create the commits in tests.
    """
    return GitUser("A committer", "committer@example.com", gpg_key_info["long_key"])


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
def sample_base_image_absolute_path(fixtures_dir):
    base_image_path = f"{fixtures_dir}/images/000001-42.600.2.tif"
    return base_image_path


@pytest.fixture(scope="session")
def temp_gpg_home_dir(tmp_path_factory, gpg_key_info, fixtures_dir):
    # Create new tmp homedir for GPG
    gnupghome = tmp_path_factory.mktemp("gnupg")

    # Apply GPG configuration
    # We need the option "allow-preset-passphrase"
    # to preset the passphrase, in order to avoid the prompt asking
    # for the passphrase while running tests.
    gpg_agent_conf_template = f"{fixtures_dir}/gpg/gpg-agent.conf"
    copy(gpg_agent_conf_template, gnupghome)
    execute_console_command(
        f"""
        gpg-connect-agent --homedir {gnupghome} RELOADAGENT /bye
    """
    )

    # Import the GPG key in the temp GPG homedir
    keygrip, signingkey, user_name, user_email = import_gpg_private_key(
        gpg_private_key=gpg_key_info["private_key"],
        passphrase=gpg_key_info["passphrase"],
        gnupghome=str(gnupghome),
    )

    # Debug: check if the GPG was imported correctly
    # execute_console_command(
    #    f"gpg --homedir {gnupghome} -k", cwd=gnupghome, print_output=True
    # )

    # Preset passphrase to avoid entering it manually while running tests
    preset_passphrase(
        gpg_key_info["keygrip"],
        passphrase=gpg_key_info["passphrase"],
        gnupghome=gnupghome,
    )

    return gnupghome
