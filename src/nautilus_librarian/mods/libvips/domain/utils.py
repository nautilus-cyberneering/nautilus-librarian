import pyvips


def get_image_dimensions(source_image_path):
    image = pyvips.Image.new_from_file(source_image_path, access="sequential")
    return image.width, image.height
