from nautilus_librarian.domain.directory import Directory
from nautilus_librarian.domain.filename import Filename


class Filepath:
    """
    A generic file path.
    """

    def __init__(self, filepath: str):
        self.directory = Directory(filepath)
        self.filename = Filename(filepath)

    def get_directory(self) -> Directory:
        return self.directory

    def get_filename(self) -> Filename:
        return self.filename

    def __eq__(self, other) -> bool:
        if isinstance(self, other.__class__):
            return (self.directory == other.directory) and (
                self.filename == other.filename
            )
        return False

    def __str__(self) -> str:
        return f"{self.directory}/{self.filename}"
