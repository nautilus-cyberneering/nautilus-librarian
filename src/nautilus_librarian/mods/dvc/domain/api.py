import dvc.api as native
from dvc.repo import Repo

# Wrappers to the native API functions
# https://dvc.org/doc/command-reference


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


def open_repo(path):
    return Repo(path)


def diff(path, a_rev="HEAD", b_rev=None, targets=None):
    repo = open_repo(path)
    return repo.diff(a_rev, b_rev, targets)


def add(path, filename, recursive=False):
    repo = open_repo(path)
    return repo.add(filename, recursive=recursive)


def status(path, remote=None, all_branches=False, recursive=False):
    repo = open_repo(path)
    return repo.status(remote=remote, all_branches=all_branches, recursive=recursive)


def push(path, targets=None, remote=None, recursive=False):
    repo = open_repo(path)
    return repo.push(targets=targets, remote=remote, recursive=recursive)


def pull(path, targets=None, remote=None, recursive=False):
    repo = open_repo(path)
    return repo.pull(targets=targets, remote=remote, recursive=recursive)


def remove(path, target: str):
    repo = open_repo(path)
    return repo.remove(target)


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
    repo = open_repo(path)
    return repo.gc(
        workspace=workspace,
        all_branches=all_branches,
        all_tags=all_tags,
        all_commits=all_commits,
        force=force,
        cloud=cloud,
        remote=remote,
    )


def list(repo_path, list_path=None, recursive=None, dvc_only=False):
    repo = Repo(repo_path)
    return repo.ls(repo_path, path=list_path, recursive=recursive, dvc_only=dvc_only)


def init(path, no_scm=False):
    from dvc.repo.init import init

    return init(root_dir=path, no_scm=no_scm)
