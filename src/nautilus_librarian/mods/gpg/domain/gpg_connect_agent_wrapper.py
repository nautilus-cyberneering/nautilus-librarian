from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.gpg.domain.validation import (
    guard_that_is_a_valid_gpg_home_dir,
    guard_that_is_a_valid_keygrip,
)


class GpgConnectAgentWrapper:
    def __init__(self, gnupghome: str) -> None:
        guard_that_is_a_valid_gpg_home_dir(gnupghome)
        self.gnupghome = gnupghome
        pass

    def preset_passphrase(self, keygrip, passphrase):
        """
        Preset passphrase using gpg-connect-agent in order to avoid prompting the user for it.
        """
        guard_that_is_a_valid_keygrip(keygrip)

        hex_passphrase = passphrase.encode("utf-8").hex().upper()

        return execute_console_command(
            "gpg-connect-agent --homedir {gnupghome} 'PRESET_PASSPHRASE {keygrip} -1 {hex_passphrase}' /bye",
            gnupghome=self.gnupghome,
            keygrip=keygrip,
            hex_passphrase=hex_passphrase,
        )


def gpg_connect_agent(gnupghome="~/.gnupg") -> GpgConnectAgentWrapper:
    return GpgConnectAgentWrapper(gnupghome)
