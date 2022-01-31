from git import Repo


class GitRepo:
    """A wrapper for GitPython Repo"""

    def __init__(self, git_repo_dir, git_user, gnupghome="~/.gnupg"):
        self.repo = Repo(git_repo_dir)
        self.git_user = git_user
        self.gnupghome = gnupghome
        self.set_git_global_user_config(git_user)

    # def add(self, filepaths):

    # def commit(self, commit_message)

    def commit(self, filepaths, commit_message):
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
        if 'added' in filepaths:
            self.repo.index.add(filepaths['added'])

        if 'deleted' in filepaths:
            self.repo.index.remove(filepaths['deleted'])

        # Write index. Needed for commit with signature:
        # https://github.com/gitpython-developers/GitPython/issues/580#issuecomment-282474086
        self.repo.index.write()

        if self.git_user.signingkey is None:
            # Unsigned commit
            return self.repo.git.commit("-m", f"{commit_message}")

        # Signed commit
        with self.repo.git.custom_environment(GNUPGHOME=self.gnupghome):
            return self.repo.git.commit(
                "-S",
                f"--gpg-sign={self.git_user.signingkey}",
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
        self.repo.config_writer().set_value(
            "user", "signingkey", git_user.signingkey
        ).release()
