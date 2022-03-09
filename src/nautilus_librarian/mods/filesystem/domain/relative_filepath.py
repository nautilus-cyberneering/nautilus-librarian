from nautilus_librarian.mods.filesystem.domain.directory import Directory
from nautilus_librarian.mods.filesystem.domain.filename import Filename
from nautilus_librarian.mods.filesystem.domain.filepath import Filepath


class NotARelativeDirectoryError(AssertionError):
    pass


class RelativeFilepath(Filepath):
    def __init__(self, filepath: str):
        self.directory = Directory(filepath)
        self.filename = Filename(filepath)
        if self.directory.is_absolute():
            raise NotARelativeDirectoryError(
                f"Expected {self.directory} to be a relative directory"
            )
