from nautilus_librarian.mods.dvc.domain.diff.path import Path
from nautilus_librarian.mods.filesystem.domain.relative_filepath import RelativeFilepath


class RenamedPath(Path):
    def __init__(self, new_path: str, old_path: str) -> None:
        self.path = RelativeFilepath(new_path)
        self.old_path = RelativeFilepath(old_path)

    def __str__(self) -> str:
        return str(self.path)

    def new(self) -> RelativeFilepath:
        return self.path

    def old(self) -> RelativeFilepath:
        return self.old_path

    def as_dict(self):
        return {
            "old": str(self.old_path),
            "new": str(self.path),
        }
