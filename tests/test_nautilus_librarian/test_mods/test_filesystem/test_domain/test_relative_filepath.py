import pytest

from nautilus_librarian.mods.filesystem.domain.relative_filepath import (
    NotARelativeDirectoryError,
    RelativeFilepath,
)


def it_should_only_allow_relative_paths():
    RelativeFilepath("data/000001/32/000001-32.600.2.tif")

    with pytest.raises(NotARelativeDirectoryError):
        RelativeFilepath("/absolute-path")


def it_should_be_comparable():
    filepath1 = RelativeFilepath("a/b/c/1.txt")
    filepath2 = RelativeFilepath("a/b/c/2.txt")

    assert filepath1 == filepath1
    assert filepath1 != filepath2
