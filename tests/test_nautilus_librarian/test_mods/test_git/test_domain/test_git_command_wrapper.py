import pytest

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.git.domain.git_command_wrapper import git


def test_get_commit_signing_key(git_temp_dir_with_one_commit, git_user):

    # Git command to get the latest commit hash
    latest_commit = execute_console_command(
        'git show --pretty=format:"%h" --no-patch', cwd=git_temp_dir_with_one_commit
    )

    signing_key = git(git_temp_dir_with_one_commit).get_commit_signing_key(
        latest_commit
    )

    assert signing_key == git_user.signingkey


def it_should_avoid_shell_injection_vulnerabilities(git_temp_dir_with_one_commit):
    commit = "779505e7575732e678e994fdef5270a94a824e12"
    commit_hash_with_malicious_code = f"{commit}; rm -rf /dir_to_be_deleted"

    with pytest.raises(Exception):
        git(git_temp_dir_with_one_commit).get_commit_signing_key(
            commit_hash_with_malicious_code
        )


def it_should_throw_an_exception_when_an_invalid_commit_rev_is_given(
    git_temp_dir_with_one_commit,
):
    invalid_commit = "invalid git rev"

    with pytest.raises(Exception):
        git(git_temp_dir_with_one_commit).get_commit_signing_key(invalid_commit)
