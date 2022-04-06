from git import Repo


class GitRepo:
    """A wrapper for GitPython Repo"""

    def __init__(self, git_repo_dir, git_user, gnupghome="~/.gnupg"):
        self.repo = Repo(git_repo_dir)
        self.git_user = git_user
        self.gnupghome = gnupghome

    def commit(self, filepaths, commit_message: str, env: dict[str, str] = {}):
        """
        It creates a commit.
        Filepath is an object with four optional file lists:
        {
            "added": [],
            "deleted": [],
            "modified": [],
            "renamed": [],
        }
        """
        if "added" in filepaths:
            self.repo.index.add(filepaths["added"])

        if "deleted" in filepaths:
            self.repo.index.remove(filepaths["deleted"])

        if "renamed" in filepaths:
            self.repo.index.add(filepaths["renamed"]["new"])
            self.repo.index.remove(filepaths["renamed"]["old"])

        # Write index. Needed for commit with signature:
        # https://github.com/gitpython-developers/GitPython/issues/580#issuecomment-282474086
        self.repo.index.write()

        # Unsigned commit
        if self.git_user.signingkey is None:
            with self.repo.git.custom_environment(**env):
                return self.repo.git.commit("-m", f"{commit_message}")

        # Signed commit
        with self.repo.git.custom_environment(GNUPGHOME=self.gnupghome, **env):
            return self.repo.git.commit(
                "-S",
                f"--gpg-sign={self.git_user.signingkey}",
                "-m",
                f"{commit_message}",
            )
