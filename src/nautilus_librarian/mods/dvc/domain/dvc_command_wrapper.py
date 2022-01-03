import json
import os

from nautilus_librarian.mods.console.domain.utils import execute_console_command


class DirNotFound(ValueError):
    pass


class DvcCommandWrapper:
    def __init__(self, git_repo_dir: str) -> None:
        self.git_repo_dir = git_repo_dir
        pass

    def default_remote(self):
        output = execute_console_command(
            "dvc remote default --project", cwd=self.git_repo_dir
        )
        return output.strip()

    def add_local_remote_as_default(self, remote_name, remote_dir):
        if not os.path.isdir(remote_dir):
            raise DirNotFound(f"Directory not found {remote_dir}")

        execute_console_command(
            "dvc remote add -d {remote_name} {remote_dir}",
            remote_name=remote_name,
            remote_dir=remote_dir,
            cwd=self.git_repo_dir,
        )

    def status_remote(self, remote_name):
        json_output = execute_console_command(
            "dvc status --show-json --cloud --remote={remote_name}",
            remote_name=remote_name,
            cwd=self.git_repo_dir,
        )
        return json.loads(json_output)


def dvc(git_repo_dir) -> DvcCommandWrapper:
    return DvcCommandWrapper(git_repo_dir)
