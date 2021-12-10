import dvc.api as native
from dvc.exceptions import OutputNotFoundError, PathMissingError
from dvc.path_info import PathInfo
from dvc.repo import Repo
import dvc.exceptions

# wrappers to the native API functions

def get_url(path, repo=None, rev=None, remote=None):
    return native.get_url(path, repo, rev, remote)

def open(  # noqa, pylint: disable=redefined-builtin
    path, repo=None, rev=None, remote=None, mode="r", encoding=None):
    return native.open(path, repo, rev, remote, mode, encoding)

def read(path, repo=None, rev=None, remote=None, mode="r", encoding=None):
    return native.read(path, repo, rev, remote, mode, encoding)

def make_checkpoint():
    return native.make_checkpoint()

def openRepo(path):
    try:
        repo = Repo(path)
    except dvc.exceptions.NotDvcRepoError:
        print("Error: Specified path does not point to a DVC repository")
    except:
        print("Unexpected error occured when opening repo at:", path)
    else:
        return repo

# Diff

def diff(path, a_rev="HEAD", b_rev=None, targets=None):
    repo = openRepo(path)
    return repo.diff(a_rev, b_rev, targets)

# Track data files

def add(path, filename, recursive=False):
    repo = openRepo(path)
    return repo.add(filename, recursive=recursive)

# Show changes in project pipelines and between remote and cache

def status(path, remote=None, all_branches=False, recursive=False):
    repo = openRepo(path)
    return repo.status(remote=remote, all_branches=all_branches, recursive=recursive)

# Upload tracked files or directories to remote storage

def push(path, targets=None, remote=None, recursive=False):
    repo = openRepo(path)
    repo.push(targets=targets, remote=remote, recursive=recursive)
        