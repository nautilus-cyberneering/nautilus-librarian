from nautilus_librarian.mods.libvips.domain.utils import get_image_dimensions


def test_get_image_dimensions(libvips_fixtures_dir):
    width, height = get_image_dimensions(libvips_fixtures_dir + "/test_image.tif")
    assert width == 512
    assert height == 256
