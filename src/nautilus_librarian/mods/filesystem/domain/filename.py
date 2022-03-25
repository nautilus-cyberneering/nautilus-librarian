import os


class Filename:
    """
    A generic filename.
    """

    def __init__(self, filename: str):
        self.filename = os.path.basename(filename)

    def __eq__(self, other) -> bool:
        if isinstance(other, Filename):
            return self.filename == other.filename
        return False

    def __str__(self) -> str:
        return self.filename
