from nautilus_librarian.mods.dvc.domain.diff.path import Path
from nautilus_librarian.mods.dvc.domain.diff.renamed_path import RenamedPath


class PathExpectedToBeStringError(AssertionError):
    pass


class InvalidPathTypeError(AssertionError):
    pass


class PathList:
    def __init__(self, paths: list[Path]) -> None:
        for path in paths:
            if not isinstance(path, Path):
                raise InvalidPathTypeError(
                    f"Path {path} is type {type(path)}. Expected to be Path."
                )
        self.paths = paths

    @staticmethod
    def from_dict_list(elements: dict):
        paths = []
        for element in elements:
            path = element["path"]
            if isinstance(path, str):
                paths.append(Path(path))
            else:
                paths.append(RenamedPath(path["new"], path["old"]))
        return PathList(paths)

    @staticmethod
    def from_string_list(elements: list[str]):
        paths = []
        for element in elements:
            path = element
            if isinstance(path, str):
                paths.append(Path(path))
            else:
                raise InvalidPathTypeError(
                    f"Path {path} is type {type(path)}. Expected to be str."
                )
        return PathList(paths)

    def __add__(self, other):
        return PathList(self.paths + other.paths)

    def __iter__(self):
        return iter(self.paths)

    def __eq__(self, other) -> bool:
        if not isinstance(other, PathList):
            return False

        if len(self.paths) != len(other.paths):
            return False

        for current_path in self.paths:
            if not other.contains(current_path):
                return False

        return True

    def __str__(self) -> str:
        return str(self.as_plain_list())

    def contains(self, path_to_find: Path) -> bool:
        for current_path in self.paths:
            if current_path == path_to_find:
                return True
        return False

    def as_plain_list(self) -> list[str]:
        return [str(path.get_value()) for path in self.paths]

    def filter(self, fn):
        return PathList(list(filter(fn, self.paths)))

    def is_empty(self) -> bool:
        return len(self.paths) == 0
