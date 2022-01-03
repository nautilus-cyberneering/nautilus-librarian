from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.gpg.domain.validation import (
    guard_that_is_a_valid_fingerprint,
    guard_that_is_a_valid_gpg_home_dir,
)


class GpgCommandWrapper:
    def __init__(self, gnupghome: str) -> None:
        guard_that_is_a_valid_gpg_home_dir(gnupghome)
        self.gnupghome = gnupghome
        pass

    def get_key_details_with_colons_format(self, fingerprint):
        guard_that_is_a_valid_fingerprint(fingerprint)

        output = execute_console_command(
            "gpg --homedir {gnupghome} --batch --with-colons --with-keygrip --list-secret-keys {fingerprint}",
            gnupghome=self.gnupghome,
            fingerprint=fingerprint,
        )
        return output


def gpg(gnupghome="~/.gnupg") -> GpgCommandWrapper:
    return GpgCommandWrapper(gnupghome)
