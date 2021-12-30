import pytest

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.git.domain.commit import get_commit_signing_key


def test_get_commit_signing_key(git_temp_dir_with_one_commit, git_user):

    # Git command to get the latest commit hash
    latest_commit = execute_console_command(
        'git show --pretty=format:"%h" --no-patch', cwd=git_temp_dir_with_one_commit
    )

    signing_key = get_commit_signing_key(
        latest_commit, cwd=git_temp_dir_with_one_commit
    )

    assert signing_key == git_user.signingkey


def it_should_avoid_shell_injection_vulnerabilities(
    git_temp_dir_with_one_commit, git_user
):
    commit = "779505e7575732e678e994fdef5270a94a824e12"
    commit_hash_with_malicious_code = f"{commit}; rm -rf /dir_to_be_deleted"

    with pytest.raises(Exception):
        get_commit_signing_key(
            commit_hash_with_malicious_code, cwd=git_temp_dir_with_one_commit
        )
