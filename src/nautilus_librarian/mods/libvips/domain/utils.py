import pyvips


def get_image(source_image_path):
    return pyvips.Image.new_from_file(source_image_path, access="sequential")


def get_image_resizing_factor(image, output_size):
    width = image.width
    height = image.height
    factor_width = output_size / width
    factor_height = output_size / height
    return min(factor_height, factor_width)


def save_image(image, destination_image_path):
    image.write_to_file(destination_image_path)


def resample_image(image, size):
    return image.resize(get_image_resizing_factor(image, size), kernel='lanczos2')


def get_image_dimensions(source_image_path):
    image = get_image(source_image_path)
    return image.width, image.height
