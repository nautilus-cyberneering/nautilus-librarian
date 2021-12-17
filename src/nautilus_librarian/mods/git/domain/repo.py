from git import Repo


class GitRepo:
    """A wrapper for GitPython Repo"""

    def __init__(self, git_repo_dir):
        self.repo = Repo(git_repo_dir)

    def create_signed_commit(self, filename, commit_message):
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

        self.repo.git.commit("-m", f"{commit_message}")
