import os
from pathlib import Path

import pytest

from nautilus_librarian.mods.console.domain.utils import execute_console_command


@pytest.fixture(scope="session")
def git_fixtures_dir():
    return os.path.dirname(Path(__file__).resolve())


@pytest.fixture()
def git_temp_dir_with_one_commit(temp_git_dir, temp_gpg_home_dir, git_user):

    # Create and initialize a git repo and add a README.md file
    execute_console_command(
        f"""
        git init
        touch README.md
        git add -A
        GNUPGHOME={temp_gpg_home_dir} git commit -S --gpg-sign={git_user.signingkey} -m "add README" --author="{git_user.name} <{git_user.email}>" # noqa
    """,
        cwd=temp_git_dir,
    )

    return temp_git_dir
