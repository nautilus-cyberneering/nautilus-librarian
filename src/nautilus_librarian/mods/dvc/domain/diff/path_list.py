from nautilus_librarian.mods.dvc.domain.diff.path import Path


class PathList:
    def __init__(self, paths: list[Path]) -> None:
        self.paths = paths

    def as_plain_list(self) -> list[Path]:
        return [str(element) for element in self.paths]
