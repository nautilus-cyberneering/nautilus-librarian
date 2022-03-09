from nautilus_librarian.mods.filesystem.domain.directory import Directory


def it_could_be_compared_to_other_to_other_directory():
    directory1 = Directory("/a/b/c")
    directory2 = Directory("/d/e/f")

    assert directory1 == directory1
    assert directory1 != directory2


def it_could_be_instantiate_from_full_file_path():
    directory = Directory("/a/b/c/1.txt")

    assert str(directory) == "/a/b/c"


def it_could_be_instantiate_from_full_dir_path():
    directory = Directory("/a/b/c/")

    assert str(directory) == "/a/b/c"


def it_could_not_be_instantiate_from_full_dir_path_without_using_a_final_forward_slash():
    """
    If there is no forward slash at the end of the string it assumes the last segment is a filename.
    """
    directory = Directory("/a/b/c")

    assert str(directory) == "/a/b"
