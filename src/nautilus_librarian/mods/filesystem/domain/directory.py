import os


class InvalidDirectoryError(AssertionError):
    pass


class MissingDirectoryError(AssertionError):
    pass


class Directory:
    """
    A generic directory.
    """

    def __init__(self, directory_or_file_path: str):
        if directory_or_file_path == "":
            raise InvalidDirectoryError(f"Invalid directory: {directory_or_file_path}")
        if os.path.dirname(directory_or_file_path) == "":
            raise MissingDirectoryError(
                f"Missing directory in path: {directory_or_file_path}"
            )
        self.directory = os.path.dirname(directory_or_file_path)

    def __eq__(self, other) -> bool:
        if isinstance(self, other.__class__):
            return self.directory == other.directory
        return False

    def __str__(self) -> str:
        return self.directory

    def is_absolute(self):
        return os.path.isabs(self.directory)
