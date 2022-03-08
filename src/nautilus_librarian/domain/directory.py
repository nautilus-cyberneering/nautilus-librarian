import os


class Directory:
    """
    A generic directory.
    """

    def __init__(self, directory: str):
        self.directory = os.path.dirname(directory)

    def __eq__(self, other) -> bool:
        if isinstance(self, other.__class__):
            return self.directory == other.directory
        return False

    def __str__(self) -> str:
        return self.directory
