from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.dvc.domain.utils import (
    extract_added_files_from_dvc_diff,
    extract_deleted_files_from_dvc_diff,
    extract_list_of_media_file_changes_from_dvc_diff_output,
    extract_modified_files_from_dvc_diff,
    extract_renamed_files_from_dvc_diff,
    get_new_filepath_if_is_a_renaming_dict,
)


def test_extract_list_of_media_file_changes_from_dvc_diff_output():
    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    filenames = extract_list_of_media_file_changes_from_dvc_diff_output(
        compact_json(dvc_diff)
    )

    assert filenames == ["000001-32.600.2.tif"]


def test_extract_added_files_from_dvc_diff():

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/000001/42/000001-42.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = extract_added_files_from_dvc_diff(compact_json(dvc_diff))

    assert result == [
        "data/000001/32/000001-32.600.2.tif",
        "data/000001/42/000001-42.600.2.tif",
    ]


def test_modified_files_from_dvc_diff():

    dvc_diff = {
        "added": [],
        "deleted": [],
        "modified": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/000001/42/000001-42.600.2.tif"},
        ],
        "renamed": [],
    }

    result = extract_modified_files_from_dvc_diff(compact_json(dvc_diff))

    assert result == [
        "000001-32.600.2.tif",
        "000001-42.600.2.tif",
    ]


def test_extract_deleted_files_from_dvc_diff():

    dvc_diff = {
        "deleted": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/000001/42/000001-42.600.2.tif"},
        ],
        "added": [],
        "modified": [],
        "renamed": [],
    }

    result = extract_deleted_files_from_dvc_diff(
        compact_json(dvc_diff), only_basename=False
    )

    assert result == [
        "data/000001/32/000001-32.600.2.tif",
        "data/000001/42/000001-42.600.2.tif",
    ]


def test_extract_renamed_files_from_dvc_diff():

    dvc_diff = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [
            {
                "path": {
                    "old": "data/000001/32/000001-32.600.2.tif",
                    "new": "data/000002/32/000002-32.600.2.tif",
                }
            }
        ],
    }

    result = extract_renamed_files_from_dvc_diff(compact_json(dvc_diff))

    assert result == [{"old": "000001-32.600.2.tif", "new": "000002-32.600.2.tif"}]


def test_get_new_path_in_a_renaming_dict():

    assert (
        get_new_filepath_if_is_a_renaming_dict(
            {
                "old": "data/000001/32/000001-32.600.2.tif",
                "new": "data/000001/32/000001-32.601.2.tif",
            }
        )
        == "data/000001/32/000001-32.601.2.tif"
    )


def test_get_path_in_a_non_renaming_dict():

    assert (
        get_new_filepath_if_is_a_renaming_dict("data/000001/32/000001-32.600.2.tif")
        == "data/000001/32/000001-32.600.2.tif"
    )
