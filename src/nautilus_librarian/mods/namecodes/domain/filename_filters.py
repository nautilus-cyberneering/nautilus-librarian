from nautilus_librarian.mods.namecodes.domain.media_library_filename import (
    MediaLibraryFilename,
)
from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    is_a_library_file,
)


def filter_media_library_files(filepaths: list[str]):
    images = list(filter(lambda filepath: is_a_library_file(filepath), filepaths))
    return images


def filter_gold_images(filepaths: list):
    media_files = filter_media_library_files(filepaths)
    gold_images = list(
        filter(
            lambda filepath: MediaLibraryFilename(filepath).is_gold_image(),
            media_files,
        )
    )
    return gold_images


def filter_base_images(filepaths: list):
    media_files = filter_media_library_files(filepaths)
    base_images = list(
        filter(
            lambda filepath: MediaLibraryFilename(filepath).is_base_image(),
            media_files,
        )
    )
    return base_images
