import pytest

from nautilus_librarian.mods.filesystem.domain.relative_filepath import (
    NotARelativeDirectoryError,
    RelativeFilepath,
)


def it_should_only_allow_relative_paths():
    with pytest.raises(NotARelativeDirectoryError):
        RelativeFilepath("/absolute-path")
