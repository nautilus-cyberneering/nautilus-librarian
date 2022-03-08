import os

from nautilus_librarian.mods.namecodes.domain.filename import MediaLibraryFilename


class FileNotFoundException(Exception):
    """Raised when an expected file is not found"""

    pass


class BaseImageNotFoundError(FileNotFoundError):
    """Raised when a Base image does not exist"""

    pass


class ExpectedGoldImageError(Exception):
    """Raised when a Gold image is expected"""

    pass


def file_locator(filename: MediaLibraryFilename) -> str:
    return f"data/{filename.artwork_id}/{filename.purpose_code}"


def get_base_image_filename_from_gold_image(
    gold_image: MediaLibraryFilename,
) -> MediaLibraryFilename:
    return gold_image.generate_base_image_filename()


def get_base_image_absolute_path_from_gold(
    git_repo_dir, gold_image: MediaLibraryFilename
):
    if not gold_image.is_gold_image:
        raise ExpectedGoldImageError(f"Expected Gold image: {gold_image}")

    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    return f"{git_repo_dir}/{corresponding_base_image_relative_path}"


def guard_that_base_image_exists(base_image_path):
    if not os.path.isfile(base_image_path):
        raise BaseImageNotFoundError(f"Missing Base image: {base_image_path}")
