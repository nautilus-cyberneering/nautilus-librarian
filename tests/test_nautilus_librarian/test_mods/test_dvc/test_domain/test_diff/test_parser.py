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


def test_dvc_diff_parser_initialization():

    dvc_diff = Parser(
        {
            "added": [],
            "deleted": [],
            "modified": [],
            "renamed": [],
        }
    )

    assert isinstance(dvc_diff, Parser)


def test_dvc_diff_parser_instantiation_from_json():

    dvc_diff_dict = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    dvc_diff = Parser.from_json(json.dumps(dvc_diff_dict))

    assert isinstance(dvc_diff, Parser)


def it_should_get_the_added_files():

    dvc_diff = Parser(
        {
            "added": [
                {"path": "folder/added_file.txt"},
            ],
            "deleted": [],
            "modified": [],
            "renamed": [],
        }
    )

    added = dvc_diff.added()

    assert added == ["folder/added_file.txt"]


def it_should_get_only_the_basenames_of_the_added_files():

    dvc_diff = Parser(
        {
            "added": [
                {"path": "folder/added_file.txt"},
            ],
            "deleted": [],
            "modified": [],
            "renamed": [],
        }
    )

    added = dvc_diff.added(only_basename=True)

    assert added == ["added_file.txt"]


def it_should_get_the_deleted_files():

    dvc_diff = Parser(
        {
            "added": [],
            "deleted": [
                {"path": "folder/deleted_file.txt"},
            ],
            "modified": [],
            "renamed": [],
        }
    )

    added = dvc_diff.deleted()

    assert added == ["folder/deleted_file.txt"]


def it_should_get_only_the_basenames_of_the_deleted_files():

    dvc_diff = Parser(
        {
            "added": [],
            "deleted": [
                {"path": "folder/deleted_file.txt"},
            ],
            "modified": [],
            "renamed": [],
        }
    )

    added = dvc_diff.deleted(only_basename=True)

    assert added == ["deleted_file.txt"]


def it_should_get_the_modified_files():

    dvc_diff = Parser(
        {
            "added": [],
            "deleted": [],
            "modified": [
                {"path": "folder/modified_file.txt"},
            ],
            "renamed": [],
        }
    )

    added = dvc_diff.modified()

    assert added == ["folder/modified_file.txt"]


def it_should_get_only_the_basenames_of_the_modified_files():

    dvc_diff = Parser(
        {
            "added": [],
            "deleted": [],
            "modified": [
                {"path": "folder/modified_file.txt"},
            ],
            "renamed": [],
        }
    )

    added = dvc_diff.modified(only_basename=True)

    assert added == ["modified_file.txt"]


def it_should_get_the_renamed_files():

    dvc_diff = Parser.from_json(dummy_full_dvc_diff())

    renamed = dvc_diff.renamed(only_basename=False)

    assert renamed == [
        {
            "old": "data/000005/32/000005-32.600.2.tif",
            "new": "data/000004/32/000004-32.600.2.tif",
        },
        {
            "old": "data/renamed-no-media-file-05.txt",
            "new": "data/renamed-no-media-file-04.txt",
        },
    ]


def it_should_get_only_the_basenames_of_the_renamed_files():

    dvc_diff = Parser.from_json(dummy_full_dvc_diff())

    renamed = dvc_diff.renamed(only_basename=True)

    assert renamed == [
        {
            "old": "000005-32.600.2.tif",
            "new": "000004-32.600.2.tif",
        },
        {
            "old": "renamed-no-media-file-05.txt",
            "new": "renamed-no-media-file-04.txt",
        },
    ]


def it_should_filter_by_type_of_change():

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

    assert dvc_diff.filter() == [
        "folder/added_file.txt",
        "folder/deleted_file.txt",
        "folder/modified_file.txt",
        "folder/renamed_file.txt",
    ]

    assert dvc_diff.filter(exclude_added=True) == [
        "folder/deleted_file.txt",
        "folder/modified_file.txt",
        "folder/renamed_file.txt",
    ]

    assert dvc_diff.filter(exclude_deleted=True) == [
        "folder/added_file.txt",
        "folder/modified_file.txt",
        "folder/renamed_file.txt",
    ]

    assert dvc_diff.filter(exclude_modified=True) == [
        "folder/added_file.txt",
        "folder/deleted_file.txt",
        "folder/renamed_file.txt",
    ]

    assert dvc_diff.filter(exclude_renamed=True) == [
        "folder/added_file.txt",
        "folder/deleted_file.txt",
        "folder/modified_file.txt",
    ]
