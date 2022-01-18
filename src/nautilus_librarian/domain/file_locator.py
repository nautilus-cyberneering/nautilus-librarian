import os

from nautilus_librarian.mods.namecodes.domain.filename import Filename


class FileNotFoundException(Exception):
    """Raised when an expected file is not found"""

    pass


class BaseImageNotFoundError(FileNotFoundError):
    """Raised when a base image does not exist"""

    pass


def file_locator(filename: Filename) -> str:
    return f"data/{filename.artwork_id}/{filename.purpose_code}"


def get_base_image_filename_from_gold_image(gold_image: Filename) -> Filename:
    return gold_image.generate_base_image_filename()


def get_base_image_absolute_path(git_repo_dir, gold_image):
    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    return f"{git_repo_dir}/{corresponding_base_image_relative_path}"


def guard_that_base_image_exists(base_image_path):
    if not os.path.isfile(base_image_path):
        raise BaseImageNotFoundError(f"Missing Base image: {base_image_path}")
