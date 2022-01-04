from nautilus_librarian.mods.libvips.domain.utils import get_image_dimensions


class file_dimensions_exception(ValueError):
    """Raised when the image dimensions are too big or too small"""

    pass


def validate_image_dimensions(filename, min_image_size: int, max_image_size: int):
    """
    It returns the image dimensions if are valid, otherwise it throws an exception.
    """
    width, height = get_image_dimensions(filename)

    if width > max_image_size or height > max_image_size:
        raise file_dimensions_exception(f"File dimensions ({width} x {height}) bigger than maximum size of {max_image_size}")

    if width < min_image_size or height < min_image_size:
        raise file_dimensions_exception(f"File dimensions ({width} x {height}) smaller than minimun size of {min_image_size}")

    return width, height
