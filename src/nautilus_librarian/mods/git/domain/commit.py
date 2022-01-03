from git import Repo

from nautilus_librarian.mods.console.domain.utils import execute_console_command


def guard_that_is_a_valid_git_rev(commit, repo_dir):
    """
    If the commit exists it returns the commit, with hhe full SHA-1 object name (40-byte hexadecimal string).
    If the commit does not exist it throws an exception.
    """
    repo = Repo(repo_dir)
    return repo.commit(commit)


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
    guard_that_is_a_valid_git_rev(commit, cwd)

    output = execute_console_command(
        "git show --show-signature --stat {commit}",
        commit=commit,
        cwd=cwd,
    )

    return extract_signing_key_id_from_signature(output)
