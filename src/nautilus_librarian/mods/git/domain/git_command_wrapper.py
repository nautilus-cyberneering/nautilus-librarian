import os

from git import Repo

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.git.domain.git_user import GitUser
from nautilus_librarian.mods.git.domain.utils import (
    extract_signing_key_id_from_signature,
)


class DirNotFound(ValueError):
    pass


class GitCommandWrapper:
    def __init__(self, git_repo_dir: str) -> None:
        if not os.path.isdir(git_repo_dir):
            raise DirNotFound(f"Directory not found {git_repo_dir}")

        self.git_repo_dir = git_repo_dir
        pass

    def guard_that_is_a_valid_git_rev(self, commit):
        """
        If the commit exists it returns the commit, with hhe full SHA-1 object name (40-byte hexadecimal string).
        If the commit does not exist it throws an exception.
        """
        repo = Repo(self.git_repo_dir)
        return repo.commit(commit)

    def get_commit_signing_key(self, commit: str) -> str:
        """
        It returns the GPG public key used to sign a commit.

        It uses the git show command. That command generates an output like this:

        gpg: Signature made mié 22 dic 2021 10:10:27 WET
        gpg:                using RSA key BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7
        gpg: Good signature from "A committer <committer@example.com>" [ultimate]
        ...

        We parse that output to get the key.

        Fingerprint: BD98B3F42545FF93EFF55F7F3F39AA1432CA6AD7
        Long key:                            3F39AA1432CA6AD7
        """
        self.guard_that_is_a_valid_git_rev(commit)

        output = execute_console_command(
            "git show --show-signature --stat {commit}",
            commit=commit,
            cwd=self.git_repo_dir,
        )

        return extract_signing_key_id_from_signature(output)

    def get_global_user(self) -> GitUser:
        """
        It returns the git global user configuration.
        It parses the config values from the git console command.
        """
        name = execute_console_command("git config --global --get user.name").strip()
        email = execute_console_command("git config --global --get user.email").strip()
        signingkey = execute_console_command(
            "git config --global --get user.signingkey"
        ).strip()

        return GitUser(name, email, signingkey)


def git(git_repo_dir=os.getcwd()) -> GitCommandWrapper:
    return GitCommandWrapper(git_repo_dir)
