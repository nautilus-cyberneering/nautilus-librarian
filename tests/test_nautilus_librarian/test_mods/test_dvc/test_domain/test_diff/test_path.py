from nautilus_librarian.mods.dvc.domain.diff.path import Path


def it_should_contain_a_relative_dir_path():

    assert (
        str(Path("data/000001/32/000001-32.600.2.tif"))
        == "data/000001/32/000001-32.600.2.tif"
    )
