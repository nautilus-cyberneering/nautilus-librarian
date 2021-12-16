from nautilus_librarian.domain.file_locator import (
    file_locator,
    get_base_image_filename_from_gold_image,
)
from nautilus_librarian.mods.namecodes.domain.filename import Filename


def test_gold_image_localization():
    gold_image_filename = Filename("000001-32.600.2.tif")

    folder = file_locator(gold_image_filename)

    assert folder == "data/000001/32"


def test_base_image_localization():
    gold_image_filename = Filename("000001-42.600.2.tif")

    folder = file_locator(gold_image_filename)

    assert folder == "data/000001/42"


def it_should_return_the_corresponding_base_image_filename_from_the_gold_image():
    gold_image_filename = Filename("000001-32.600.2.tif")

    base_image_filename = get_base_image_filename_from_gold_image(gold_image_filename)

    assert base_image_filename == Filename("000001-42.600.2.tif")
