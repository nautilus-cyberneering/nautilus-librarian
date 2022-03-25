import os

from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.mods.namecodes.domain.media_library_filename import (
    MediaLibraryFilename,
)


class InvalidImageFolderException(ValueError):
    """Raised when the file is located in a wrong path"""

    pass


def validate_filepath(filepath):
    actual_folder = os.path.dirname(filepath)

    filename = MediaLibraryFilename(os.path.basename(filepath))

    expected_folder = file_locator(filename)

    if expected_folder != actual_folder:
        raise InvalidImageFolderException(
            f'Invalid folder for image. The file "{ filepath }" should be in the folder "{ expected_folder }"'
        )


def validate_filepaths(filepaths):
    for filepath in filepaths:
        validate_filepath(filepath)
