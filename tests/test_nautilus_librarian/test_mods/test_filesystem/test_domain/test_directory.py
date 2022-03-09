import pytest

from nautilus_librarian.mods.filesystem.domain.directory import (
    Directory,
    InvalidDirectoryError,
)


def it_should_not_be_empty():
    with pytest.raises(InvalidDirectoryError):
        Directory("")


def it_could_be_compared_to_other_to_other_directory():
    directory1 = Directory("/a/b/c")
    directory2 = Directory("/d/e/f")

    assert directory1 == directory1
    assert directory1 != directory2


def it_could_be_instantiate_from_full_file_path():
    assert str(Directory("/a/b/c/1.txt")) == "/a/b/c"
    assert str(Directory("/a/b/c/1")) == "/a/b/c"
    assert str(Directory("/a/b/c/")) == "/a/b/c"


def it_could_be_instantiate_from_full_dir_path():
    directory = Directory("/a/b/c/")

    assert str(directory) == "/a/b/c"


def it_should_indicate_wether_the_dir_is_an_absolute_path_or_not():
    absolute_directory = Directory("/a/b/c")

    assert absolute_directory.is_absolute()

    relative_directory = Directory("./a/b/c")

    assert not relative_directory.is_absolute()
