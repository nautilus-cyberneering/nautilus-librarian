from nautilus_librarian.mods.libvips.domain.utils import (
    get_image,
    get_image_dimensions,
    get_image_icc_profile,
    modify_icc_profile,
)


def test_get_image_dimensions(libvips_fixtures_dir):
    width, height = get_image_dimensions(libvips_fixtures_dir + "/test_image.tif")
    assert width == 512
    assert height == 256


def test_get_image_icc_profile(libvips_fixtures_dir):
    image = get_image(libvips_fixtures_dir + "/test_image_adobergb.tif")
    assert "Adobe RGB" in f"{get_image_icc_profile(image)}"


def test_modify_image_icc_profile(libvips_fixtures_dir):
    image = get_image(libvips_fixtures_dir + "/test_image_adobergb.tif")
    assert "sRGB" not in f"{get_image_icc_profile(image)}"
    image = modify_icc_profile(image, "sRGB")
    assert "sRGB" in f"{get_image_icc_profile(image)}"
