from nautilus_librarian.domain.directory import Directory
from nautilus_librarian.domain.filename import Filename
from nautilus_librarian.domain.filepath import Filepath


def it_could_be_compared_to_other_filepath():
    filepath1 = Filepath("/a/b/c/1.txt")
    filepath2 = Filepath("/a/b/c/2.txt")

    assert filepath1 == filepath1
    assert filepath1 != filepath2


def it_could_be_instantiate_from_full_file_path():
    filepath = Filepath("/a/b/c/1.txt")

    assert str(filepath) == "/a/b/c/1.txt"


def it_should_return_the_file_name():
    filepath = Filepath("/a/b/c/1.txt")

    assert filepath.get_filename() == Filename("1.txt")


def it_should_return_the_directory():
    filepath = Filepath("/a/b/c/1.txt")

    assert filepath.get_directory() == Directory("/a/b/c/")
