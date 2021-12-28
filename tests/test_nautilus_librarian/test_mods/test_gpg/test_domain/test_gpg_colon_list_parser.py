import pytest

from nautilus_librarian.mods.gpg.domain.gpg_colon_list_parser import GpgColonListParser


@pytest.fixture(scope="session")
def sample_gpg_output():
    return """
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


def test_instantiation():
    gpgColonListParser = GpgColonListParser("output")
    assert isinstance(gpgColonListParser, GpgColonListParser)


def it_should_extract_the_keygrip_for_a_key_searching_by_its_fingerprint(
    sample_gpg_output,
):
    gpgColonListParser = GpgColonListParser(sample_gpg_output)

    keygrip = gpgColonListParser.get_keygrip_by_fingerprint(
        "88966A5B8C01BD04F3DA440427304EDD6079B81C"
    )

    assert keygrip == "449972AC9FF11BCABEED8A7AE834C4349CC4DBFF"


def it_should_return_none_if_it_does_not_find_the_fingerprint_when_it_is_searching_for_a_keygrip(
    sample_gpg_output,
):
    gpgColonListParser = GpgColonListParser(sample_gpg_output)

    keygrip = gpgColonListParser.get_keygrip_by_fingerprint("non existing fingerprint")

    assert keygrip is None


def it_should_extract_the_user_id_for_a_key_searching_by_its_fingerprint(
    sample_gpg_output,
):

    gpgColonListParser = GpgColonListParser(sample_gpg_output)

    name, email = gpgColonListParser.get_user_id_by_fingerprint(
        "88966A5B8C01BD04F3DA440427304EDD6079B81C"
    )

    assert name == "A committer"
    assert email == "committer@example.com"


def it_should_return_none_if_it_does_not_find_the_fingerprint_when_it_is_searching_for_a_user_id(
    sample_gpg_output,
):
    gpgColonListParser = GpgColonListParser(sample_gpg_output)

    name, email = gpgColonListParser.get_user_id_by_fingerprint(
        "non existing fingerprint"
    )

    assert name is None
    assert email is None
