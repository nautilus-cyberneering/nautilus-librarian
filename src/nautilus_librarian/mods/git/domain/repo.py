from git import Repo


class GitRepo:
    """A wrapper for GitPython Repo"""

    def __init__(self, git_repo_dir, git_global_user):
        self.repo = Repo(git_repo_dir)
        self.git_global_user = git_global_user
        self.set_git_global_user_config(git_global_user)

    def commit(self, filepaths, commit_message):
        """
        It creates a commit
        """
        self.repo.index.add(filepaths)

        # Write index. Needed for commit with signature:
        # https://github.com/gitpython-developers/GitPython/issues/580#issuecomment-282474086
        self.repo.index.write()

        if self.git_global_user.signingkey is None:
            # Unsigned commit
            return self.repo.git.commit("-m", f"{commit_message}")

        # Signed commit
        return self.repo.git.commit(
            "-S",
            f"--gpg-sign={self.git_global_user.signingkey}",
            "-m",
            f"{commit_message}",
        )

    def set_git_global_user_config(self, git_user):
        """
        This configuration prevents from having this git error:
        stderr: 'Committer identity unknown
        *** Please tell me who you are.
        Run
        git config --global user.email "you@example.com"
        git config --global user.name "Your Name"
        to set your account's default identity.
        Omit --global to set the identity only in this repository.
        fatal: unable to auto-detect email address (got 'root@b37fb619ac5a.(none)')'
        """
        self.repo.config_writer().set_value("user", "name", git_user.name).release()
        self.repo.config_writer().set_value("user", "email", git_user.email).release()
