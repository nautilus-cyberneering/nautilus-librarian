from nautilus_librarian.mods.filesystem.domain.directory import Directory
from nautilus_librarian.mods.filesystem.domain.filename import Filename
from nautilus_librarian.mods.filesystem.domain.filepath import Filepath


class NotAnAbsoluteDirectoryError(AssertionError):
    pass


class AbsoluteFilepath(Filepath):
    def __init__(self, filepath: str):
        self.directory = Directory(filepath)
        self.filename = Filename(filepath)
        if not self.directory.is_absolute():
            raise NotAnAbsoluteDirectoryError(
                f"Expected {self.directory} to be an absolute directory"
            )
