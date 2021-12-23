import dvc.api as native
import dvc.exceptions
from dvc.repo import Repo

# wrappers to the native API functions


def get_url(path, repo=None, rev=None, remote=None):
    return native.get_url(path, repo, rev, remote)


def open(  # noqa, pylint: disable=redefined-builtin
    path, repo=None, rev=None, remote=None, mode="r", encoding=None
):
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
    except dvc.exceptions.DvcException:
        print("Unexpected error occurred when opening repo at:", path)
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
    return repo.push(targets=targets, remote=remote, recursive=recursive)


# Download tracked files from the remote storage


def pull(path, targets=None, remote=None, recursive=False):
    repo = openRepo(path)
    return repo.pull(targets=targets, remote=remote, recursive=recursive)


# Remove stages from dvc.yaml and/or stop tracking files or directories
# (untested)


def remove(path, target: str):
    repo = openRepo(path)
    return repo.remove(target)


# Remove unused files and directories from cache or remote storage


def gc(
    path,
    workspace=False,
    all_branches=False,
    all_tags=False,
    all_commits=False,
    force=False,
    cloud=False,
    remote=None,
):
    repo = openRepo(path)
    return repo.gc(
        workspace=workspace,
        all_branches=all_branches,
        all_tags=all_tags,
        all_commits=all_commits,
        force=force,
        cloud=cloud,
        remote=remote,
    )


# List project contents, including files, models, and directories tracked by DVC and by Git


def list(repo_path, list_path=None, recursive=None, dvc_only=False):
    repo = Repo(repo_path)
    return repo.ls(repo_path, path=list_path, recursive=recursive, dvc_only=dvc_only)


# Creates an empty repo on the given directory


def init(path, no_scm=False):
    from dvc.repo.init import init

    return init(root_dir=path, no_scm=no_scm)
