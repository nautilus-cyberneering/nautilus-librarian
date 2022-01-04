import os

from nautilus_librarian.mods.gpg.domain.exceptions import (
    DirNotFound,
    InvalidFingerprint,
    InvalidKeygrip,
)
from nautilus_librarian.mods.gpg.domain.utils import is_hexadecimal


def guard_that_is_a_valid_gpg_home_dir(gnupghome):
    if not os.path.isdir(gnupghome):
        raise DirNotFound(f"Directory {gnupghome} not found")


def guard_that_is_a_valid_fingerprint(fingerprint):
    if len(fingerprint) != 40:
        raise InvalidFingerprint(f"Invalid fingerprint {fingerprint}")

    if not is_hexadecimal(fingerprint):
        raise InvalidFingerprint(f"Invalid fingerprint {fingerprint}")


def guard_that_is_a_valid_keygrip(keygrip):
    if len(keygrip) != 40:
        raise InvalidKeygrip(f"Invalid keygrip {keygrip}")

    if not is_hexadecimal(keygrip):
        raise InvalidKeygrip(f"Invalid keygrip {keygrip}")
