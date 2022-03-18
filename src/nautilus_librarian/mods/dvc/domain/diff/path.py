from nautilus_librarian.mods.filesystem.domain.relative_filepath import RelativeFilepath


class Path:
    def __init__(self, path: str) -> None:
        self.path = RelativeFilepath(path)

    def __eq__(self, other) -> bool:
        if isinstance(other, Path):
            return self.path == other.path
        return False

    def __str__(self) -> str:
        return str(self.path)
