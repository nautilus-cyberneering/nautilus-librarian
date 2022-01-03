def extract_signing_key_id_from_signature(signature_info):
    """
    It extract the signingley if from the git signature info.

    From this text:
    gpg: Signature made mié 22 dic 2021 10:10:27 WET
    gpg:                using RSA key BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7
    gpg: Good signature from "A committer <committer@example.com>" [ultimate]

    It returns the key in the long format: 3F39AA1432CA6AD7
    """
    lines = signature_info.splitlines()
    line_with_key = lines[2]
    fingerprint = line_with_key[-40:]
    long_key = fingerprint[-16:]
    return long_key
