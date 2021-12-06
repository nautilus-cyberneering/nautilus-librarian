# We are not implementing multiple transformations yet.
# {ARTWORK_ID}-{PURPOSE_CODE}.{TRANSFORMATION_CODE}.{TYPE_CODE}.{EXTENSION}

from nautilus_librarian.mods.namecodes.domain.parse_filename import parse_filename


class FilenameException(Exception):
    """Raised when the filename format is invalid"""

    pass


def validate_artwork_id(artwork_id):
    if artwork_id == "":
        raise ValueError(
            "Missing artwork id. Artwork id should be between 000000 and 099999"
        )
    if len(artwork_id) != 6:
        raise ValueError(
            "Invalid artwork length. Artwork id should have 6 digits. For example: 099999"
        )
    if int(artwork_id) < 0 or int(artwork_id) > 99999:
        raise ValueError(
            "Wrong artwork id. Artwork id should be between 000000 and 099999"
        )


def validate_purpose_code(purpose_code):
    if purpose_code == "":
        raise ValueError("Missing purpose code. Purpose code should be: 32 or 42")
    if int(purpose_code) not in [32, 42]:
        raise ValueError("Wrong purpose code. Purpose code should be: 32 or 42")


def validate_transformation_code(transformation_code):
    if transformation_code == "":
        raise ValueError(
            "Missing transformation code. Transformation code should be: 600"
        )
    if int(transformation_code) not in [600]:
        raise ValueError(
            "Wrong transformation code. Transformation code should be: 600"
        )


def validate_type_code(type_code):
    if type_code == "":
        raise ValueError("Missing type code. Type code should be: 2")
    if type_code != "2":
        raise ValueError("Wrong type code. Type code should be: 2")


def validate_extension(extension):
    if extension == "":
        raise ValueError("Missing extension. Extension should be: tif")
    if extension != "tif":
        raise ValueError("Wrong extension. Extension should be: tif")


def validate_filename(filename):
    (
        artwork_id,
        purpose_code,
        transformation_code,
        type_code,
        extension,
    ) = parse_filename(filename)

    validate_artwork_id(artwork_id)
    validate_purpose_code(purpose_code)
    validate_transformation_code(transformation_code)
    validate_type_code(type_code)
    validate_extension(extension)


def validate_filenames(filenames):
    for filename in filenames:
        try:
            validate_filename(filename)
        except ValueError as error:
            raise FilenameException(f"Invalid filename {filename}. {error}")
