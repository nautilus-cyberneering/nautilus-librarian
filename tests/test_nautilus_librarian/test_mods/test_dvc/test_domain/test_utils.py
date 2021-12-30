from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.dvc.domain.utils import (
    extract_added_files_from_dvc_diff,
    extract_list_of_media_file_changes_from_dvc_diff_output,
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
