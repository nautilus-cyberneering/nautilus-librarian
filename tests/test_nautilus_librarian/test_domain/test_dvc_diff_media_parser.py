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


def test_extract_all_changed_files_from_dvc_diff():

    files = extract_all_changed_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=False
    )

    expected_files = [
        "data/000001/32/000001-32.600.2.tif",
        "data/000002/32/000002-32.600.2.tif",
        "data/000003/32/000003-32.600.2.tif",
        "data/000004/32/000004-32.600.2.tif",
    ]

    assert files == expected_files

    files = extract_all_changed_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=True
    )

    expected_files = [
        "000001-32.600.2.tif",
        "000002-32.600.2.tif",
        "000003-32.600.2.tif",
        "000004-32.600.2.tif",
    ]

    assert files == expected_files


def test_extract_deleted_files_from_dvc_diff():

    result = extract_deleted_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=False
    )

    assert result == [
        "data/000002/32/000002-32.600.2.tif",
    ]

    result = extract_deleted_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=True
    )

    assert result == [
        "000002-32.600.2.tif",
    ]


def test_extract_added_and_modified_files_from_dvc_diff():

    result = extract_added_and_modified_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=False
    )

    assert result == [
        "data/000001/32/000001-32.600.2.tif",
        "data/000003/32/000003-32.600.2.tif",
    ]

    result = extract_added_and_modified_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=True
    )

    assert result == [
        "000001-32.600.2.tif",
        "000003-32.600.2.tif",
    ]


def test_modified_files_from_dvc_diff():

    result = extract_modified_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=False
    )

    assert result == [
        "data/000003/32/000003-32.600.2.tif",
    ]

    result = extract_modified_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=True
    )

    assert result == [
        "000003-32.600.2.tif",
    ]


def test_extract_renamed_files_from_dvc_diff():

    result = extract_renamed_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=False
    )

    assert result == [
        {
            "old": "data/000005/32/000005-32.600.2.tif",
            "new": "data/000004/32/000004-32.600.2.tif",
        }
    ]

    result = extract_renamed_files_from_dvc_diff(
        dummy_full_dvc_diff(), only_basename=True
    )

    assert result == [{"old": "000005-32.600.2.tif", "new": "000004-32.600.2.tif"}]


def test_extract_list_of_new_or_renamed_files_from_dvc_diff_output():

    filenames = extract_list_of_new_and_renamed_files_from_dvc_diff_output(
        dummy_full_dvc_diff()
    )

    assert filenames == [
        "data/000001/32/000001-32.600.2.tif",  # We include only the new name of the file for renamed ones.
        "data/000004/32/000004-32.600.2.tif",  # We include only the new name of the file for renamed ones.
    ]
