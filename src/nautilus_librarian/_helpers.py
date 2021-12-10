"""General Helper Functions"""

import errno
import os
from pathlib import Path


def get_path_to_project_root() -> Path:
    """Gets the Path Object for the Project Root, by testing for 'pyproject.toml'"""

    path: Path = Path(__file__).parent

    while path.joinpath("pyproject.toml").exists() is not True:
        if path.home() == path:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), str(path.absolute())
            )
        if len(str(path.absolute())) == 1:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), str(path.absolute())
            )

        path = path.parent

    return path


def path_to_pyproject_toml() -> Path:
    """Get pyproject.toml from relative path."""

    path: Path = get_path_to_project_root().joinpath("pyproject.toml")
    if path.exists() is not True:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), str(path.absolute())
        )

    return path


def get_unicode_document(path: Path) -> str:
    """Get the Toml Document from Path"""

    document: str

    with path.open(mode="r", buffering=-1, encoding="utf8") as document_file:
        document = document_file.read()

    return document
