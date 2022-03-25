from nautilus_librarian.mods.dvc.domain.diff.path import Path
from nautilus_librarian.mods.dvc.domain.diff.path_list import (
    InvalidPathTypeError,
    PathList,
)
from nautilus_librarian.mods.dvc.domain.diff.renamed_path import RenamedPath


class RenamedPathList(PathList):
    def __init__(self, paths: list[Path]) -> None:
        for path in paths:
            if not isinstance(path, RenamedPath):
                raise InvalidPathTypeError(
                    f"Path {path} is type {type(path)}. Expected to be Path."
                )
        self.paths = paths
