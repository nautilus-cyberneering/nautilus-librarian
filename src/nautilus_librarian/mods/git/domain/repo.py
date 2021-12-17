from git import Repo


class GitRepo:
    """A wrapper for GitPython Repo"""

    def __init__(self, git_repo_dir):
        self.repo = Repo(git_repo_dir)

    def create_signed_commit(self, filename, commit_message, signingkey):
        """
        It creates a signed commit.

        WIP: signed commit is not created yet.

        Example how to sign:
        https://github.com/josecelano/pygithub/blob/main/src/03_sign_commit_using_the_gitpython_package.py#L190
        """
        index = self.repo.index
        index.add([filename])

        # Write index. Needed for commit with signature:
        # https://github.com/gitpython-developers/GitPython/issues/580#issuecomment-282474086
        index.write()

        if signingkey is None:
            return self.repo.git.commit("-m", f"{commit_message}")

        return self.repo.git.commit(
            "-S", f"--gpg-sign={signingkey}", "-m", f"{commit_message}"
        )

    def set_git_global_user_config(self, user_name, user_email):
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
        self.repo.config_writer().set_value("user", "name", user_name).release()
        self.repo.config_writer().set_value("user", "email", user_email).release()
