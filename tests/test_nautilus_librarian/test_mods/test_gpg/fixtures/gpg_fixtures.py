import os
from pathlib import Path
from shutil import copy

import pytest

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.gpg.domain.utils import (
    import_gpg_private_key,
    preset_passphrase,
)


@pytest.fixture(scope="session")
def gpg_fixtures_dir():
    return os.path.dirname(Path(__file__).resolve())


@pytest.fixture(scope="session")
def gpg_master_key_info():
    """
    The GPG master key info. This key is used in tests. Key details:

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
    """

    return {
        "fingerprint": "88966A5B8C01BD04F3DA440427304EDD6079B81C",
        "long_key": "440427304EDD6079B81C",
        "keygrip": "449972AC9FF11BCABEED8A7AE834C4349CC4DBFF",
        "name": "A committer",
        "email": "committer@example.com",
    }


@pytest.fixture(scope="session")
def gpg_signing_key_info(gpg_fixtures_dir):
    """
    The GPG subkey key used to sign the commits in tests. Key details:

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
    committer_gpg_private_key_path = f"{gpg_fixtures_dir}/committer_private_key.pgp"
    gpg_private_key = "-----BEGIN PGP PRIVATE KEY BLOCK-----\n\n"
    with open(committer_gpg_private_key_path, "r") as f:
        gpg_private_key += f.read()
    gpg_private_key += "\n\n-----END PGP PRIVATE KEY BLOCK-----\n"
    # secretlint-enable

    return {
        "fingerprint": "BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7",
        "long_key": "3F39AA1432CA6AD7",
        "keygrip": "00CB9308AE0B6DE018C5ADBAB29BA7899D6062BE",
        "passphrase": "123456",
        "private_key": gpg_private_key,
        "name": "A committer",
        "email": "committer@example.com",
    }


@pytest.fixture(scope="session")
def temp_gpg_home_dir(tmp_path_factory, gpg_signing_key_info, gpg_fixtures_dir):
    # Create new tmp homedir for GPG
    gnupghome = tmp_path_factory.mktemp("gnupg")

    # Apply GPG configuration
    # We need the option "allow-preset-passphrase"
    # to preset the passphrase, in order to avoid the prompt asking
    # for the passphrase while running tests.
    gpg_agent_conf_template = f"{gpg_fixtures_dir}/gpg-agent.conf"
    copy(gpg_agent_conf_template, gnupghome)
    execute_console_command(
        """
        gpg-connect-agent --homedir {gnupghome} RELOADAGENT /bye
    """,
        gnupghome=gnupghome,
    )

    # Import the GPG key in the temp GPG homedir
    import_gpg_private_key(
        gpg_private_key=gpg_signing_key_info["private_key"],
        passphrase=gpg_signing_key_info["passphrase"],
        gnupghome=str(gnupghome),
    )

    # Preset passphrase to avoid entering it manually while running tests
    preset_passphrase(
        gpg_signing_key_info["keygrip"],
        passphrase=gpg_signing_key_info["passphrase"],
        gnupghome=gnupghome,
    )

    return gnupghome
