import gnupg

from nautilus_librarian.mods.console.domain.utils import execute_console_command


def get_key_details_with_colons_format(fingerprint):
    output = execute_console_command(
        f"gpg --batch --with-colons --with-keygrip --list-secret-keys {fingerprint}"
    )
    return output


def get_keygrip_by(fingerprint):
    """
    This function gets the keygrip of a given GPG key using the gpg console command and parsing the output.

    Sample output for the command:
    sec:-:4096:1:27304EDD6079B81C:1637342753:::-:::scESC:::+:::23::0:
    fpr:::::::::88966A5B8C01BD04F3DA440427304EDD6079B81C:
    grp:::::::::449972AC9FF11BCABEED8A7AE834C4349CC4DBFF:
    uid:-::::1637342753::B3B0B2247600E80BAB9D4802D5CF0AFC477DE016::A committer <committer@example.com>::::::::::0:
    ssb:-:4096:1:5B6BDD35BEDFBF6F:1637342753::::::e:::+:::23:
    fpr:::::::::B1D4A2483D1D2A02416BE0775B6BDD35BEDFBF6F:
    grp:::::::::97D36F5B8F5BECDA8A1923FC00D11C7C438584F9:
    In that example the keygrip (grp) of the key 88966A5B8C01BD04F3DA440427304EDD6079B81C is
    449972AC9FF11BCABEED8A7AE834C4349CC4DBFF
    Specification for the format: https://github.com/CSNW/gnupg/blob/master/doc/DETAILS
    """

    output = get_key_details_with_colons_format(fingerprint)

    records = output.split("\n")

    current_fingerprint = ""

    for record in records:
        if record.startswith("fpr"):
            fields = record.split(":")
            current_fingerprint = fields[9]
        if record.startswith("grp"):
            fields = record.split(":")
            keygrip = fields[9]
            if current_fingerprint == fingerprint:
                return keygrip

    return None


def get_key_user_by(fingerprint):
    """
    This function gets the uid record of a given GPG key using the gpg console command and parsing the output.

    Sample output for the command:
    sec:-:4096:1:27304EDD6079B81C:1637342753:::-:::scESC:::+:::23::0:
    fpr:::::::::88966A5B8C01BD04F3DA440427304EDD6079B81C:
    grp:::::::::449972AC9FF11BCABEED8A7AE834C4349CC4DBFF:
    uid:-::::1637342753::B3B0B2247600E80BAB9D4802D5CF0AFC477DE016::A committer <committer@example.com>::::::::::0:
    ssb:-:4096:1:5B6BDD35BEDFBF6F:1637342753::::::e:::+:::23:
    fpr:::::::::B1D4A2483D1D2A02416BE0775B6BDD35BEDFBF6F:
    grp:::::::::97D36F5B8F5BECDA8A1923FC00D11C7C438584F9:
    In that example the 'uid' of the key 88966A5B8C01BD04F3DA440427304EDD6079B81C is A committer <committer@example.com>
    There could be more than one 'uid' record. We return the first one.
    Specification for the format: https://github.com/CSNW/gnupg/blob/master/doc/DETAILS
    """

    output = get_key_details_with_colons_format(fingerprint)

    records = output.split("\n")

    current_fingerprint = ""

    for record in records:
        if record.startswith("fpr"):
            fields = record.split(":")
            current_fingerprint = fields[9]
        if record.startswith("uid"):
            fields = record.split(":")
            uid = fields[9]
            if current_fingerprint == fingerprint:
                name, separator, rest = uid.partition(" <")
                email, separator, rest = rest.partition(">")
                return name, email

    return None


def get_short_key_id_from_fingerprint(fingerprint):
    """
    fingerprint = 88966A5B8C01BD04F3DA440427304EDD6079B81C
    Fingerprint: 8896 6A5B 8C01 BD04  F3DA 4404 2730 4EDD 6079 B81C
    Long key ID:                                2730 4EDD 6079 B81C
    Short key ID:                                         6079 B81C
    Returns: 6079B81C
    """
    return fingerprint[24:]


def import_gpg_private_key(gpg_private_key, passphrase, gnupghome):
    """
    Import PGP key into the the local keyring
    """
    gpg = gnupg.GPG(gnupghome=gnupghome, verbose=False, use_agent=True)

    import_result = gpg.import_keys(gpg_private_key, passphrase=passphrase)
    fingerprint = import_result.fingerprints[0]

    keygrip = get_keygrip_by(fingerprint)
    committer_name, committer_email = get_key_user_by(fingerprint)

    short_key_id = get_short_key_id_from_fingerprint(fingerprint)

    # print(f'Fingerprint: {fingerprint}')
    # print(f'Short key ID: {short_key_id}')
    # print(f'Keygrip: {keygrip}')
    # print(f'Commiter name: {committer_name}')
    # print(f'Committer email: {committer_email}')

    return keygrip, short_key_id, committer_name, committer_email


def preset_passphrase(keygrip, passphrase, gnupghome):
    """
    Preset passphrase using gpg-connect-agent in order to avoid prompting the user for it.
    """
    hex_passphrase = passphrase.encode("utf-8").hex().upper()
    preset_passphrase_command = f"gpg-connect-agent --homedir {gnupghome} 'PRESET_PASSPHRASE {keygrip} -1 {hex_passphrase}' /bye"  # noqa
    return execute_console_command(preset_passphrase_command)
