from nautilus_librarian.domain.file_locator import (
    file_locator,
    get_base_image_filename_from_gold_image,
)
from nautilus_librarian.mods.namecodes.domain.media_library_filename import (
    MediaLibraryFilename,
)


def test_gold_image_localization():
    gold_image_filename = MediaLibraryFilename("000001-32.600.2.tif")

    folder = file_locator(gold_image_filename)

    assert folder == "data/000001/32"


def test_base_image_localization():
    gold_image_filename = MediaLibraryFilename("000001-52.600.2.tif")

    folder = file_locator(gold_image_filename)

    assert folder == "data/000001/52"


def it_should_return_the_corresponding_base_image_filename_from_the_gold_image():
    gold_image_filename = MediaLibraryFilename("000001-32.600.2.tif")

    base_image_filename = get_base_image_filename_from_gold_image(gold_image_filename)

    assert base_image_filename == MediaLibraryFilename("000001-52.600.2.tif")
