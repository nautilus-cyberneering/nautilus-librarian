from nautilus_librarian.mods.dvc.domain.diff.path import Path
from nautilus_librarian.mods.dvc.domain.diff.path_list import PathList
from nautilus_librarian.mods.dvc.domain.diff.renamed_path import RenamedPath


def it_should_contain_a_list_of_dvc_diff_paths():

    file_path_1 = Path("data/000001/32/000001-32.600.2.tif")
    file_path_2 = Path("data/000002/32/000002-32.600.2.tif")

    path_list = PathList([file_path_1, file_path_2])

    assert path_list.as_plain_list() == [
        "data/000001/32/000001-32.600.2.tif",
        "data/000002/32/000002-32.600.2.tif",
    ]


def it_should_return_the_new_file_path_for_a_renamed_path():

    path = RenamedPath("data/new.txt", "data/old.txt")

    path_list = PathList([path])

    assert path_list.as_plain_list() == ["data/new.txt"]


def it_should_be_instantiable_from_a_list_of_dictionaries():

    path_list = PathList.from_dict_list(
        [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/000002/32/000002-32.600.2.tif"},
        ]
    )

    assert path_list.as_plain_list() == [
        "data/000001/32/000001-32.600.2.tif",
        "data/000002/32/000002-32.600.2.tif",
    ]


def it_should_be_instantiable_from_a_list_of_dictionaries_using_renamed_paths():

    path_list = PathList.from_dict_list(
        [
            {
                "path": {
                    "old": "data/000001/32/000001-32.600.2.tif",
                    "new": "data/000002/32/000002-32.600.2.tif",
                }
            }
        ]
    )

    assert path_list.as_plain_list() == ["data/000002/32/000002-32.600.2.tif"]


def it_should_allow_to_add_two_path_lists():

    path_list_1 = PathList.from_string_list(["data/000001/32/000001-32.600.2.tif"])
    path_list_2 = PathList.from_string_list(["data/000002/32/000002-32.600.2.tif"])

    path_list = path_list_1 + path_list_2

    assert path_list.as_plain_list() == [
        "data/000001/32/000001-32.600.2.tif",
        "data/000002/32/000002-32.600.2.tif",
    ]


def it_should_be_iterable():

    file_path_1 = Path("data/000001/32/000001-32.600.2.tif")
    file_path_2 = Path("data/000002/32/000002-32.600.2.tif")
    file_paths = [file_path_1, file_path_2]

    path_list = PathList(file_paths)

    for index, item in enumerate(path_list):
        assert item == file_paths[index]


def it_should_be_comparable():

    path_list_1 = PathList.from_string_list(["data/000001/32/000001-32.600.2.tif"])
    same_path_list_as_path_list_1 = PathList.from_string_list(
        ["data/000001/32/000001-32.600.2.tif"]
    )

    path_list_2 = PathList.from_string_list(["data/000002/32/000002-32.600.2.tif"])

    assert path_list_1 == same_path_list_as_path_list_1
    assert path_list_1 != path_list_2


def it_should_allow_to_check_if_it_contains_a_given_path():

    file_path_1 = Path("data/000001/32/000001-32.600.2.tif")
    file_path_2 = Path("data/000002/32/000002-32.600.2.tif")

    path_list = PathList([file_path_1])

    assert path_list.contains(file_path_1)
    assert not path_list.contains(file_path_2)


def it_should_allow_to_filter_paths_using_a_function():

    file_path_1 = Path("data/000001/32/000001-32.600.2.tif")
    file_path_2 = Path("data/000002/32/000002-32.600.2.tif")

    path_list = PathList([file_path_1, file_path_2])

    filtered_path_list = path_list.filter(
        lambda path: str(path) == "data/000001/32/000001-32.600.2.tif"
    )

    expected_filtered_path_list = PathList.from_string_list(
        ["data/000001/32/000001-32.600.2.tif"]
    )

    assert filtered_path_list == expected_filtered_path_list


def it_could_be_empty():

    path_list = PathList([])

    assert path_list.is_empty()
