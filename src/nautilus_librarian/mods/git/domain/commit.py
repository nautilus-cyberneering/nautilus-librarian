from nautilus_librarian.mods.console.domain.utils import execute_console_command


def get_commit_signing_key(commit: str, cwd):
    """
    It returns the GPG public key used to sign a commit.

    It uses the git show command. That command generates an output like this:

    gpg: Signature made mié 22 dic 2021 10:10:27 WET
    gpg:                using RSA key BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7
    gpg: Good signature from "A committer <committer@example.com>" [ultimate]
    ...

    We need to parse that output to get the key.

    Fingerprint: BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7
    Long key:                            3F39AA1432CA6AD7
    """
    output = execute_console_command(
        "git show --show-signature --stat {commit}",
        commit=commit,
        cwd=cwd,
    )

    # Extract long key from output
    lines = output.splitlines()
    line_with_key = lines[2]
    fingerprint = line_with_key[-40:]
    long_key = fingerprint[-16:]

    return long_key
