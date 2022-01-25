import os.path

import dvc.api as native
from dvc.repo import Repo as DvcRepo
from git import Repo as GitRepo

from nautilus_librarian.mods.console.domain.utils import (
    change_current_working_directory,
)
from nautilus_librarian.mods.dvc.domain.dvc_command_wrapper import dvc


class InvalidDvcDir(AssertionError):
    pass


class DvcApiWrapper:
    """
    Wrapper for the native API functions.

    More info about the native DVC api: https://dvc.org/doc/command-reference
    More info about the DVC commands: https://dvc.org/doc/api-reference

    TODO: find out how we can remove the "change_current_working_directory" call before
    running extended API methods.
    """

    def __init__(self, repo_path):
        if not os.path.isdir(repo_path):
            raise InvalidDvcDir(f"No dvc initialization found in dir {repo_path}")
        self.repo_path = repo_path
        self.git_repo = GitRepo(self.repo_path)
        self.dvc_repo = DvcRepo(self.repo_path)

    @staticmethod
    def git_init(path):
        return GitRepo.init(path)

    @staticmethod
    def dvc_init(path, no_scm=False):
        return DvcRepo.init(root_dir=path, no_scm=no_scm)

    @staticmethod
    def init(path, no_scm=False):
        DvcApiWrapper.git_init(path)
        DvcApiWrapper.dvc_init(path, no_scm)

    # Native API methods

    def get_url(self, path, repo=None, rev=None, remote=None):
        return native.get_url(path, self.repo_path, rev, remote)

    def open(self, path, repo=None, rev=None, remote=None, mode="r", encoding=None):
        return native.open(path, self.repo_path, rev, remote, mode, encoding)

    def read(self, path, repo=None, rev=None, remote=None, mode="r", encoding=None):
        return native.read(path, self.repo_path, rev, remote, mode, encoding)

    def make_checkpoint(self):
        return native.make_checkpoint()

    # Extended dvc.repo methods

    def diff(self, a_rev="HEAD", b_rev=None, targets=None):
        change_current_working_directory(self.repo_path)
        return self.dvc_repo.diff(a_rev, b_rev, targets)

    def add(self, filename, recursive=False):
        change_current_working_directory(self.repo_path)
        return self.dvc_repo.add(filename, recursive=recursive)

    def status(self, remote=None, all_branches=False, recursive=False):
        change_current_working_directory(self.repo_path)
        return self.dvc_repo.status(
            remote=remote, all_branches=all_branches, recursive=recursive
        )

    def push(self, targets=None, remote=None, recursive=False):
        change_current_working_directory(self.repo_path)
        return self.dvc_repo.push(targets=targets, remote=remote, recursive=recursive)

    def pull(self, targets=None, remote=None, recursive=False):
        change_current_working_directory(self.repo_path)
        return self.dvc_repo.pull(targets=targets, remote=remote, recursive=recursive)

    def remove(self, target: str):
        change_current_working_directory(self.repo_path)
        return self.dvc_repo.remove(target)

    def move(self, from_path: str, to_path: str):
        change_current_working_directory(self.repo_path)
        return self.dvc_repo.move(from_path, to_path)

    def gc(
        self,
        workspace=False,
        all_branches=False,
        all_tags=False,
        all_commits=False,
        force=False,
        cloud=False,
        remote=None,
    ):
        change_current_working_directory(self.repo_path)
        return self.dvc_repo.gc(
            workspace=workspace,
            all_branches=all_branches,
            all_tags=all_tags,
            all_commits=all_commits,
            force=force,
            cloud=cloud,
            remote=remote,
        )

    def list(self, list_path=None, recursive=None, dvc_only=False):
        return self.dvc_repo.ls(
            self.repo_path, path=list_path, recursive=recursive, dvc_only=dvc_only
        )

    # Wrappers for console commands

    def dvc_default_remote(self):
        """
        It returns the default remote for the dvc repo.
        """
        return dvc(self.repo_path).default_remote()
