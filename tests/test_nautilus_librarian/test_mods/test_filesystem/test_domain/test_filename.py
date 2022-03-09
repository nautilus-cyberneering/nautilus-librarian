from nautilus_librarian.mods.filesystem.domain.filename import Filename


def it_could_be_compared_to_other_filename():
    filename1 = Filename("1.txt")
    filename2 = Filename("2.txt")

    assert filename1 == filename1
    assert filename1 != filename2


def it_could_be_instantiate_from_full_file_path():
    filename = Filename("/a/b/c/1.txt")

    assert str(filename) == "1.txt"
