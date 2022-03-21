from nautilus_librarian.mods.filesystem.domain.relative_filepath import RelativeFilepath


class Path:
    def __init__(self, value: str) -> None:
        self.value = RelativeFilepath(value)

    def __eq__(self, other) -> bool:
        if isinstance(other, Path):
            return self.value == other.value
        return False

    def get_value(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return str(self.value)
