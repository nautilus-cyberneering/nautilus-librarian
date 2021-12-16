from nautilus_librarian.mods.namecodes.domain.filename import Filename


def file_locator(filename: Filename) -> str:
    return f"data/{filename.artwork_id}/{filename.purpose_code}"
