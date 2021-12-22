from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.typer.commands.workflows.actions.auto_commit_base_images import (
    files_to_commit,
    get_new_gold_images_filenames_from_dvc_diff,
)


def test_get_new_gold_images_from_dvc_diff():

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/000001/42/000001-42.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = get_new_gold_images_filenames_from_dvc_diff(compact_json(dvc_diff))

    assert result == [Filename("data/000001/32/000001-32.600.2.tif")]


def test_files_to_commit():
    filepaths = files_to_commit("data/000001/42/000001-42.600.2.tif")

    assert filepaths == [
        "data/000001/42/.gitignore",
        "data/000001/42/000001-42.600.2.tif.dvc",
    ]
