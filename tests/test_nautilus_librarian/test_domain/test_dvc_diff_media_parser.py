from test_nautilus_librarian.test_mods.test_dvc.test_domain.test_diff.test_parser import (
    dummy_full_dvc_diff,
)

from nautilus_librarian.domain.dvc_diff_media_parser import (
    extract_added_and_modified_files_from_dvc_diff,
    extract_all_changed_files_from_dvc_diff,
    extract_deleted_files_from_dvc_diff,
    extract_list_of_new_and_renamed_files_from_dvc_diff_output,
    extract_modified_files_from_dvc_diff,
    extract_renamed_files_from_dvc_diff,
)
from nautilus_librarian.mods.dvc.domain.diff.path_list import PathList


def test_extract_all_changed_files_from_dvc_diff():

    files = extract_all_changed_files_from_dvc_diff(dummy_full_dvc_diff())

    expected_files = PathList.from_string_list(
        [
            "data/000001/32/000001-32.600.2.tif",
            "data/000002/32/000002-32.600.2.tif",
            "data/000003/32/000003-32.600.2.tif",
            "data/000004/32/000004-32.600.2.tif",
        ]
    ).as_plain_list()

    assert files == expected_files


def test_extract_deleted_files_from_dvc_diff():

    path_list = extract_deleted_files_from_dvc_diff(dummy_full_dvc_diff())

    expected_path_list = PathList.from_string_list(
        [
            "data/000002/32/000002-32.600.2.tif",
        ]
    ).as_plain_list()

    assert path_list == expected_path_list


def test_extract_added_and_modified_files_from_dvc_diff():

    path_list = extract_added_and_modified_files_from_dvc_diff(dummy_full_dvc_diff())

    expected_path_list = PathList.from_string_list(
        [
            "data/000001/32/000001-32.600.2.tif",
            "data/000003/32/000003-32.600.2.tif",
        ]
    ).as_plain_list()

    assert path_list == expected_path_list


def test_modified_files_from_dvc_diff():

    path_list = extract_modified_files_from_dvc_diff(dummy_full_dvc_diff())

    expected_path_list = PathList.from_string_list(
        ["data/000003/32/000003-32.600.2.tif"]
    ).as_plain_list()

    assert path_list == expected_path_list


def test_extract_renamed_files_from_dvc_diff():

    path_list = extract_renamed_files_from_dvc_diff(dummy_full_dvc_diff())

    expected_path_list = PathList.from_dict_list(
        [
            {
                "path": {
                    "old": "data/000005/32/000005-32.600.2.tif",
                    "new": "data/000004/32/000004-32.600.2.tif",
                }
            }
        ]
    )

    assert path_list == expected_path_list


def test_extract_list_of_new_or_renamed_files_from_dvc_diff_output():

    path_list = extract_list_of_new_and_renamed_files_from_dvc_diff_output(
        dummy_full_dvc_diff()
    )

    expected_path_list = PathList.from_dict_list(
        [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {
                "path": {
                    "old": "data/000005/32/000005-32.600.2.tif",
                    "new": "data/000004/32/000004-32.600.2.tif",
                }
            },
        ]
    )

    assert path_list == expected_path_list
