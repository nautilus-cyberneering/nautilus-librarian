from nautilus_librarian.mods.git.domain.utils import (
    extract_signing_key_id_from_signature,
)


def test_extract_signing_key_id_from_signature():
    long_key = extract_signing_key_id_from_signature(
        """
    gpg: Signature made mié 22 dic 2021 10:10:27 WET
    gpg:                using RSA key BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7
    gpg: Good signature from "A committer <committer@example.com>" [ultimate]
    """
    )

    assert long_key == "3F39AA1432CA6AD7"
