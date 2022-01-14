import os

from nautilus_librarian.mods.libvips.domain.utils import (
    get_image,
    modify_icc_profile,
    resample_image,
    save_image,
)


def create_output_folder(destination_filename):
    os.makedirs(os.path.dirname(destination_filename), exist_ok=True)


def process_image(
    filename, destination_filename: str, base_image_size: int, icc_profile: str
):
    """
    Generates and saves an image file using a source image, with the specified size
    """
    image = get_image(filename)
    image = resample_image(image, base_image_size)
    image = modify_icc_profile(image, icc_profile)
    create_output_folder(destination_filename)
    save_image(image, destination_filename)
