from nautilus_librarian.mods.dvc.domain.diff.path import Path
from nautilus_librarian.mods.filesystem.domain.relative_filepath import RelativeFilepath


class RenamedPath(Path):
    def __init__(self, value: str, old_value: str) -> None:
        super().__init__(value)
        self.old_value = RelativeFilepath(old_value)

    def __str__(self) -> str:
        return f"{str(self.old_value)} -> {str(self.value)}"

    def new(self) -> RelativeFilepath:
        return self.value

    def old(self) -> RelativeFilepath:
        return self.old_value

    def as_dict(self):
        return {
            "old": str(self.old_value),
            "new": str(self.value),
        }
