from test_nautilus_librarian.test_mods.test_dvc.test_domain.test_diff.test_parser import dummy_full_dvc_diff
from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.dvc.domain.diff.path_list import PathList
from nautilus_librarian.mods.dvc.domain.utils import extract_added_files_from_dvc_diff


def test_extract_added_files_from_dvc_diff():

    path_list = extract_added_files_from_dvc_diff(dummy_full_dvc_diff())

    expected_path_list = PathList.from_string_list(
        [
            "data/000001/32/000001-32.600.2.tif",
            "data/added-no-media-file-01.txt",
        ]
    ).as_plain_list()

    assert path_list == expected_path_list
