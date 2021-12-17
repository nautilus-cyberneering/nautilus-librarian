from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.dvc.domain.utils import (
    extract_modified_media_file_list_from_dvd_diff_output,
    extract_new_gold_images_from_dvc_diff,
)


def test_extract_modified_media_file_list_from_dvd_diff_output():
    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    filenames = extract_modified_media_file_list_from_dvd_diff_output(
        compact_json(dvc_diff)
    )

    assert filenames == ["000001-32.600.2.tif"]


def test_extract_new_gold_images_from_dvc_diff():

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},  # Gold image
            # {"path": "data/000001/42/000001-42.600.2.tif"}, # Base image
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = extract_new_gold_images_from_dvc_diff(compact_json(dvc_diff))

    assert result == ["data/000001/32/000001-32.600.2.tif"]
