import os

from nautilus_librarian.mods.namecodes.domain.filename import Filename


class FilepathException(Exception):
    """Raised when the file is located in a wrong path"""

    pass


def validate_filepath(filepath):
    # data/000001/32/000001-32.600.2.tif

    basename = os.path.basename(filepath)

    filename = Filename(basename)

    print(filename)


def parse_filename(filename):
    artwork_id, char, rest = filename.partition("-")
    purpose_code, char, rest = rest.partition(".")
    transformation_code, char, rest = rest.partition(".")
    type_code, char, rest = rest.partition(".")
    extension, char, rest = rest.partition(".")
    return artwork_id, purpose_code, transformation_code, type_code, extension
