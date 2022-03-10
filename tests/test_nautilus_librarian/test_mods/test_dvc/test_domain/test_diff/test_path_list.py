from nautilus_librarian.mods.dvc.domain.diff.path import Path
from nautilus_librarian.mods.dvc.domain.diff.path_list import PathList
from nautilus_librarian.mods.dvc.domain.diff.renamed_path import RenamedPath


def it_should_contain_a_list_of_dvc_diff_paths():

    file_path1 = Path("data/000001/32/000001-32.600.2.tif")
    file_path2 = Path("data/000002/32/000002-32.600.2.tif")

    path_list = PathList([file_path1, file_path2])

    assert path_list.as_plain_list() == [
        "data/000001/32/000001-32.600.2.tif",
        "data/000002/32/000002-32.600.2.tif",
    ]


def it_return_the_new_file_path_for_a_renamed_path():

    path = RenamedPath("data/new.txt", "data/old.txt")

    path_list = PathList([path])

    assert path_list.as_plain_list() == ["data/new.txt"]
