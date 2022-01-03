from nautilus_librarian.mods.libvips.domain.utils import get_image_dimensions


class FileDimensionsException(ValueError):
    """Raised when the image dimensions are too big or too small"""

    pass


def validate_image_dimensions(filename):
    """
    It returns true if the image dimensions are valid, otherwise it throws an exception.
    """
    width, height = get_image_dimensions(filename)

    if width > 100 or height < 100:
        raise FileDimensionsException("File width or height is bigger than expected")

    if width > 10000 or height > 10000:
        raise FileDimensionsException("File width or height is smaller than expected")

    return True
