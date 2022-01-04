from nautilus_librarian.mods.libvips.domain.utils import get_image_dimensions


class FileDimensionsException(ValueError):
    """Raised when the image dimensions are too big or too small"""

    pass


def validate_image_dimensions(filename, min_image_size, max_image_size):
    """
    It returns true if the image dimensions are valid, otherwise it throws an exception.
    """
    width, height = get_image_dimensions(filename)

    if width > max_image_size or height > max_image_size:
        raise FileDimensionsException("File width or height is bigger than expected")

    if width < min_image_size or height < min_image_size:
        raise FileDimensionsException("File width or height is smaller than expected")

    return True
