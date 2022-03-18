import pytest

from nautilus_librarian.mods.filesystem.domain.absolute_filepath import (
    AbsoluteFilepath,
    NotAnAbsoluteDirectoryError,
)


def it_should_only_allow_absolute_paths():
    with pytest.raises(NotAnAbsoluteDirectoryError):
        AbsoluteFilepath("./relative-path")


def it_should_be_comparable():
    filepath1 = AbsoluteFilepath("/a/b/c/1.txt")
    filepath2 = AbsoluteFilepath("/a/b/c/2.txt")

    assert filepath1 == filepath1
    assert filepath1 != filepath2
