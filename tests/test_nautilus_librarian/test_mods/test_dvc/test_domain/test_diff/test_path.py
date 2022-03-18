from nautilus_librarian.mods.dvc.domain.diff.path import Path


def it_should_contain_a_relative_dir_path():

    assert (
        str(Path("data/000001/32/000001-32.600.2.tif"))
        == "data/000001/32/000001-32.600.2.tif"
    )


def it_should_be_comparable():

    path_1 = Path("data/000001/32/000001-32.600.2.tif")
    same_path_as_path_1 = Path("data/000001/32/000001-32.600.2.tif")
    path_2 = Path("data/000002/32/000002-32.600.2.tif")

    assert path_1 == same_path_as_path_1
    assert path_1 != path_2
