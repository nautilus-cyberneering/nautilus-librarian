import os

import gnupg

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.gpg.domain.gpg_colon_list_parser import GpgColonListParser


class InvalidFingerprint(ValueError):
    pass


def is_hexadecimal(text):
    try:
        int(text, 16)
        return True
    except ValueError:
        return False


def guard_that_is_a_valid_fingerprint(fingerprint):
    if len(fingerprint) != 40:
        raise InvalidFingerprint(f"Invalid fingerprint {fingerprint}")

    if not is_hexadecimal(fingerprint):
        raise InvalidFingerprint(f"Invalid fingerprint {fingerprint}")


def guard_that_is_a_valid_keygrip(keygrip):
    if len(keygrip) != 40:
        raise InvalidFingerprint(f"Invalid keygrip {keygrip}")

    if not is_hexadecimal(keygrip):
        raise InvalidFingerprint(f"Invalid keygrip {keygrip}")


def guard_that_is_a_valid_gpg_home_dir(gnupghome):
    if not os.path.isdir(gnupghome):
        raise ValueError(f"Directory {gnupghome} not found")


def get_key_details_with_colons_format(fingerprint, gnupghome):
    guard_that_is_a_valid_fingerprint(fingerprint)
    guard_that_is_a_valid_gpg_home_dir(gnupghome)

    output = execute_console_command(
        "gpg --homedir {gnupghome} --batch --with-colons --with-keygrip --list-secret-keys {fingerprint}",
        gnupghome=gnupghome,
        fingerprint=fingerprint,
    )
    return output


def get_keygrip_by(fingerprint, gnupghome):
    """
    This function gets the keygrip of a given GPG key using the gpg console command and parsing the output.

    Sample output for the command:

    sec:-:4096:1:27304EDD6079B81C:1637342753:::-:::cESC:::+:::23::0:
    fpr:::::::::88966A5B8C01BD04F3DA440427304EDD6079B81C:
    grp:::::::::449972AC9FF11BCABEED8A7AE834C4349CC4DBFF:
    uid:-::::1638182580::B3B0B2247600E80BAB9D4802D5CF0AFC477DE016::A committer <committer@example.com>::::::::::0:
    ssb:-:4096:1:5B6BDD35BEDFBF6F:1637342753::::::e:::+:::23:
    fpr:::::::::B1D4A2483D1D2A02416BE0775B6BDD35BEDFBF6F:
    grp:::::::::97D36F5B8F5BECDA8A1923FC00D11C7C438584F9:
    ssb:-:4096:1:3F39AA1432CA6AD7:1637931661::::::s:::+:::23:
    fpr:::::::::BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7:
    grp:::::::::00CB9308AE0B6DE018C5ADBAB29BA7899D6062BE:

    In that example the keygrip (grp) of the key 88966A5B8C01BD04F3DA440427304EDD6079B81C is
    449972AC9FF11BCABEED8A7AE834C4349CC4DBFF
    Specification for the format: https://github.com/CSNW/gnupg/blob/master/doc/DETAILS
    """

    output = get_key_details_with_colons_format(fingerprint, gnupghome)

    gpgColonListParser = GpgColonListParser(output)

    return gpgColonListParser.get_keygrip_by_fingerprint(fingerprint)


def get_key_user_by(fingerprint, gnupghome):
    """
    This function gets the uid record of a given GPG key using the gpg console command and parsing the output.

    Sample output for the command:

    sec:-:4096:1:27304EDD6079B81C:1637342753:::-:::cESC:::+:::23::0:
    fpr:::::::::88966A5B8C01BD04F3DA440427304EDD6079B81C:
    grp:::::::::449972AC9FF11BCABEED8A7AE834C4349CC4DBFF:
    uid:-::::1638182580::B3B0B2247600E80BAB9D4802D5CF0AFC477DE016::A committer <committer@example.com>::::::::::0:
    ssb:-:4096:1:5B6BDD35BEDFBF6F:1637342753::::::e:::+:::23:
    fpr:::::::::B1D4A2483D1D2A02416BE0775B6BDD35BEDFBF6F:
    grp:::::::::97D36F5B8F5BECDA8A1923FC00D11C7C438584F9:
    ssb:-:4096:1:3F39AA1432CA6AD7:1637931661::::::s:::+:::23:
    fpr:::::::::BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7:
    grp:::::::::00CB9308AE0B6DE018C5ADBAB29BA7899D6062BE:

    In that example the 'uid' of the key 88966A5B8C01BD04F3DA440427304EDD6079B81C is A committer <committer@example.com>
    There could be more than one 'uid' record. We return the first one.
    Specification for the format: https://github.com/CSNW/gnupg/blob/master/doc/DETAILS
    """

    output = get_key_details_with_colons_format(fingerprint, gnupghome)

    gpgColonListParser = GpgColonListParser(output)

    return gpgColonListParser.get_user_id_by_fingerprint(fingerprint)


def import_gpg_private_key(gpg_private_key, passphrase, gnupghome):
    """
    Import PGP key into the the local keyring.
    It returns the fingerprint of the imported key.
    """
    gpg = gnupg.GPG(gnupghome=gnupghome, verbose=False, use_agent=True)

    return gpg.import_keys(gpg_private_key, passphrase=passphrase)


def preset_passphrase(keygrip, passphrase, gnupghome):
    """
    Preset passphrase using gpg-connect-agent in order to avoid prompting the user for it.
    """
    guard_that_is_a_valid_gpg_home_dir(gnupghome)
    guard_that_is_a_valid_keygrip(keygrip)

    hex_passphrase = passphrase.encode("utf-8").hex().upper()
    return execute_console_command(
        "gpg-connect-agent --homedir {gnupghome} 'PRESET_PASSPHRASE {keygrip} -1 {hex_passphrase}' /bye",
        gnupghome=gnupghome,
        keygrip=keygrip,
        hex_passphrase=hex_passphrase,
    )
