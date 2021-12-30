from nautilus_librarian.mods.dvc.domain.dvc_diff_parser import DvcDiffParser


def extract_added_and_modified_and_renamed_files_from_dvc_diff(
    dvc_diff_json, only_basename=True
):
    """
    It gets a plain string list with the added, modified or renamed files from the dvc diff json.

    With only_basename=True
    Input: {"added": [{"path": "data/000001/32/000001-32.600.2.tif"}], "deleted": [], "modified": [], "renamed": []}
    Output: ['000001-32.600.2.tif']

    only_basename=False
    Input: {"added": [{"path": "data/000001/32/000001-32.600.2.tif"}], "deleted": [], "modified": [], "renamed": []}
    Output: ['data/000001/32/000001-32.600.2.tif']
    """
    dvc_diff = DvcDiffParser.from_json(dvc_diff_json)
    return dvc_diff.filter(exclude_deleted=True, only_basename=only_basename)


def extract_added_and_modified_files_from_dvc_diff(dvc_diff_json, only_basename=True):
    """
    It gets a plain string list with the added and modified files from the dvc diff json.

    With only_basename=True
    Input: {"added": [{"path": "data/000001/32/000001-32.600.2.tif"}], "deleted": [], "modified": [], "renamed": []}
    Output: ['000001-32.600.2.tif']

    only_basename=False
    Input: {"added": [{"path": "data/000001/32/000001-32.600.2.tif"}], "deleted": [], "modified": [], "renamed": []}
    Output: ['data/000001/32/000001-32.600.2.tif']
    """
    dvc_diff = DvcDiffParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_deleted=True, exclude_renamed=True, only_basename=only_basename
    )


def extract_list_of_media_file_changes_from_dvc_diff_output(
    dvc_diff, only_basename=True
):
    return extract_added_and_modified_and_renamed_files_from_dvc_diff(
        dvc_diff, only_basename
    )


def extract_added_files_from_dvc_diff(dvc_diff_json):
    """
    Parses the list of added Gold images from dvc diff output in json format.

    Input:
    dvc_diff
    {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/000001/42/000001-42.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    Output:
    ["000001-32.600.2.tif"]
    Notice Base image should not be included in the result.
    """
    dvc_diff = DvcDiffParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_deleted=True, exclude_modified=True, exclude_renamed=True
    )
