import pytest

from nautilus_librarian.mods.libvips.domain.validate_image_dimensions import (
    validate_image_dimensions,
    file_dimensions_exception
)


def it_should_reject_image_bigger_than_expected(libvips_fixtures_dir):

    with pytest.raises(file_dimensions_exception):
        validate_image_dimensions(libvips_fixtures_dir + "/test_image.tif", 8, 16)


def it_should_reject_image_smaller_than_expected(libvips_fixtures_dir):

    with pytest.raises(file_dimensions_exception):
        validate_image_dimensions(libvips_fixtures_dir + "/test_image.tif", 4096, 8192)


def it_should_accept_proper_size_image(libvips_fixtures_dir):

    assert(validate_image_dimensions(libvips_fixtures_dir + "/test_image.tif", 256, 8192))