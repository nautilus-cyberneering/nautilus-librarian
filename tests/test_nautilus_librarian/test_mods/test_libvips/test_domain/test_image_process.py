from nautilus_librarian.mods.libvips.domain.process_image import process_image
from nautilus_librarian.mods.libvips.domain.utils import (
    get_image,
    get_image_dimensions,
    get_image_icc_profile,
)


def it_should_generate_a_256_x_128_image(tmp_path_factory, libvips_fixtures_dir):
    output_path = tmp_path_factory.mktemp("repo")
    process_image(
        f"{libvips_fixtures_dir}/test_image.tif",
        f"{output_path}/output_image.tif",
        256,
        "sRGB",
    )
    width, height = get_image_dimensions(f"{output_path}/output_image.tif")
    assert width == 256
    assert height == 128
    image = get_image(f"{output_path}/output_image.tif")
    assert "sRGB" in f"{get_image_icc_profile(image)}"
