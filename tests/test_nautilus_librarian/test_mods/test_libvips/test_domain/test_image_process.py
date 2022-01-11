from nautilus_librarian.mods.libvips.domain.process_image import process_image
from nautilus_librarian.mods.libvips.domain.utils import get_image_dimensions


def it_should_generate_a_256_x_128_image(tmp_path_factory, libvips_fixtures_dir):
    output_path = tmp_path_factory.mktemp("repo")
    process_image(
        f"{libvips_fixtures_dir}/test_image.tif", f"{output_path}/output_image.tif", 256
    )
    width, height = get_image_dimensions(f"{output_path}/output_image.tif")
    assert width == 256
    assert height == 128
