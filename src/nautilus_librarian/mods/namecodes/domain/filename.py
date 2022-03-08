import os.path
from enum import Enum


class PurposeCode(Enum):
    GOLD_INDEX = 30
    GOLD_METADATA = 31
    GOLD_IMAGE = 32
    BASE_INDEX = 50
    BASE_METADATA = 51
    BASE_IMAGE = 52

    def __str__(self):
        return "%s" % self.value


class TypeCode(Enum):
    INDEX = 0
    METADATA = 1
    IMAGE = 2

    def __str__(self):
        return "%s" % self.value


class MediaLibraryFilename:
    """
    A media library file name.

    It allows you to create an invalid filename because the parser do not fail.
    We could use the "validate_filename" function in the constructor but the final
    filename specification is not defined yet. We will probably use a json schema
    to validate and parse the filename.
    """

    def __init__(self, filename):
        basename = os.path.basename(filename)
        self.filename = basename
        self.parse(self.filename)

    def parse(self, filename):
        self.artwork_id, char, rest = filename.partition("-")
        self.purpose_code, char, rest = rest.partition(".")
        self.transformation_code, char, rest = rest.partition(".")
        self.type_code, char, rest = rest.partition(".")
        self.extension, char, rest = rest.partition(".")

    def parts(self):
        return (
            self.artwork_id,
            self.purpose_code,
            self.transformation_code,
            self.type_code,
            self.extension,
        )

    def is_gold_image(self):
        return self.purpose_code == str(
            PurposeCode.GOLD_IMAGE
        ) and self.type_code == str(TypeCode.IMAGE)

    def is_base_image(self):
        return self.purpose_code == str(
            PurposeCode.BASE_IMAGE
        ) and self.type_code == str(TypeCode.IMAGE)

    def generate_base_image_filename(self):
        return MediaLibraryFilename(
            f"""{self.artwork_id}-{str(PurposeCode.BASE_IMAGE)}.{self.transformation_code}.{self.type_code}.{self.extension}"""  # noqa
        )

    def __eq__(self, other):
        if isinstance(other, MediaLibraryFilename):
            return self.filename == other.filename
        return False

    def __str__(self):
        return self.filename
