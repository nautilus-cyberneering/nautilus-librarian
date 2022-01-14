import os

from nautilus_librarian.mods.namecodes.domain.filename import Filename


class FileNotFoundException(Exception):
    """Raised when an expected file is not found"""

    pass


def file_locator(filename: Filename) -> str:
    return f"data/{filename.artwork_id}/{filename.purpose_code}"


def get_base_image_filename_from_gold_image(gold_image: Filename) -> Filename:
    return gold_image.generate_base_image_filename()


def guard_that_base_image_exists(base_image_path):
    if not os.path.isfile(base_image_path):
        raise FileNotFoundException(f"Missing Base image: {base_image_path}")
