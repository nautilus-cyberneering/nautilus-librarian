import json

from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.dvc.domain.diff.parser import Parser


def dummy_full_dvc_diff():
    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/added-no-media-file-01.txt"},
        ],
        "deleted": [
            {"path": "data/000002/32/000002-32.600.2.tif"},
            {"path": "data/deleted-no-media-file-02.txt"},
        ],
        "modified": [
            {"path": "data/000003/32/000003-32.600.2.tif"},
            {"path": "data/modified-no-media-file-03.txt"},
        ],
        "renamed": [
            {
                "path": {
                    "old": "data/000005/32/000005-32.600.2.tif",
                    "new": "data/000004/32/000004-32.600.2.tif",
                },
            },
            {
                "path": {
                    "old": "data/renamed-no-media-file-05.txt",
                    "new": "data/renamed-no-media-file-04.txt",
                }
            },
        ],
    }
    return compact_json(dvc_diff)


def it_should_instantiate_from_a_json():

    dvc_diff_dict = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    dvc_diff = Parser.from_json(json.dumps(dvc_diff_dict))

    assert isinstance(dvc_diff, Parser)


def it_should_allow_to_filter_by_type_of_change():

    dvc_diff = Parser(
        {
            "added": [
                {"path": "folder/added_file.txt"},
            ],
            "deleted": [
                {"path": "folder/deleted_file.txt"},
            ],
            "modified": [
                {"path": "folder/modified_file.txt"},
            ],
            "renamed": [
                {"path": "folder/renamed_file.txt"},
            ],
        }
    )

    assert dvc_diff.filter().as_plain_list() == [
        "folder/added_file.txt",
        "folder/deleted_file.txt",
        "folder/modified_file.txt",
        "folder/renamed_file.txt",
    ]

    assert dvc_diff.filter(exclude_added=True).as_plain_list() == [
        "folder/deleted_file.txt",
        "folder/modified_file.txt",
        "folder/renamed_file.txt",
    ]

    assert dvc_diff.filter(exclude_deleted=True).as_plain_list() == [
        "folder/added_file.txt",
        "folder/modified_file.txt",
        "folder/renamed_file.txt",
    ]

    assert dvc_diff.filter(exclude_modified=True).as_plain_list() == [
        "folder/added_file.txt",
        "folder/deleted_file.txt",
        "folder/renamed_file.txt",
    ]

    assert dvc_diff.filter(exclude_renamed=True).as_plain_list() == [
        "folder/added_file.txt",
        "folder/deleted_file.txt",
        "folder/modified_file.txt",
    ]
