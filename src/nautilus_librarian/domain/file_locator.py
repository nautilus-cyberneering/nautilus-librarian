from nautilus_librarian.mods.namecodes.domain.filename import Filename


def file_locator(filename: Filename) -> str:
    return f"data/{filename.artwork_id}/{filename.purpose_code}"


def get_base_image_filename_from_gold_image(gold_image: Filename) -> Filename:
    return gold_image.generate_base_image_filename()
