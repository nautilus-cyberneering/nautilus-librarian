import pytest

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.git.domain.commit import (
    extract_signing_key_id_from_signature,
    get_commit_signing_key,
)


def test_get_commit_signing_key(git_temp_dir_with_one_commit, git_user):

    # Git command to get the latest commit hash
    latest_commit = execute_console_command(
        'git show --pretty=format:"%h" --no-patch', cwd=git_temp_dir_with_one_commit
    )

    signing_key = get_commit_signing_key(
        latest_commit, cwd=git_temp_dir_with_one_commit
    )

    assert signing_key == git_user.signingkey


def test_extract_signing_key_id_from_signature():
    long_key = extract_signing_key_id_from_signature(
        """
    gpg: Signature made mié 22 dic 2021 10:10:27 WET
    gpg:                using RSA key BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7
    gpg: Good signature from "A committer <committer@example.com>" [ultimate]
    """
    )

    assert long_key == "3F39AA1432CA6AD7"


def it_should_avoid_shell_injection_vulnerabilities(
    git_temp_dir_with_one_commit, git_user
):
    commit = "779505e7575732e678e994fdef5270a94a824e12"
    commit_hash_with_malicious_code = f"{commit}; rm -rf /dir_to_be_deleted"

    with pytest.raises(Exception):
        get_commit_signing_key(
            commit_hash_with_malicious_code, cwd=git_temp_dir_with_one_commit
        )


def it_should_throw_an_exception_when_an_invalid_commit_rev_is_given(
    git_temp_dir_with_one_commit, git_user
):
    invalid_commit = "invalid git rev"

    with pytest.raises(Exception):
        get_commit_signing_key(invalid_commit, cwd=git_temp_dir_with_one_commit)
