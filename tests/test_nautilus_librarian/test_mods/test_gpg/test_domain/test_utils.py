from nautilus_librarian.mods.gpg.domain.utils import (
    get_key_details_with_colons_format,
    get_key_user_by,
    get_keygrip_by,
)


def remove_white_spaces_and_line_breaks(text):
    return text.replace(" ", "").replace("\n", "")


def test_get_key_details_with_colons_format(temp_gpg_home_dir, gpg_signing_key_info):
    output = get_key_details_with_colons_format(
        gpg_signing_key_info["fingerprint"], temp_gpg_home_dir
    )

    expected_output = """
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
    """

    assert remove_white_spaces_and_line_breaks(
        output
    ) == remove_white_spaces_and_line_breaks(expected_output)


def test_get_keygrip_by(temp_gpg_home_dir, gpg_signing_key_info):
    keygrip = get_keygrip_by(gpg_signing_key_info["fingerprint"], temp_gpg_home_dir)

    assert keygrip == gpg_signing_key_info["keygrip"]


def test_get_key_user_by(temp_gpg_home_dir, gpg_master_key_info):
    name, email = get_key_user_by(gpg_master_key_info["fingerprint"], temp_gpg_home_dir)

    assert name == gpg_master_key_info["name"]
    assert email == gpg_master_key_info["email"]


def test_get_key_user_without_uid_record(temp_gpg_home_dir, gpg_signing_key_info):
    name, email = get_key_user_by(
        gpg_signing_key_info["fingerprint"], temp_gpg_home_dir
    )

    assert name is None
    assert email is None
