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


def extract_all_changed_files_from_dvc_diff(dvc_diff_json, only_basename=True):
    """
    It gets a plain string list with the added, modified, deleted or renamed files from the dvc diff json.

    With only_basename=True
    Input: {"added": [{"path": "data/000001/32/000001-32.600.2.tif"}], "deleted": [], "modified": [], "renamed": []}
    Output: ['000001-32.600.2.tif']

    only_basename=False
    Input: {"added": [{"path": "data/000001/32/000001-32.600.2.tif"}], "deleted": [], "modified": [], "renamed": []}
    Output: ['data/000001/32/000001-32.600.2.tif']
    """
    dvc_diff = DvcDiffParser.from_json(dvc_diff_json)
    return dvc_diff.filter(only_basename=only_basename)


def extract_deleted_files_from_dvc_diff(dvc_diff_json, only_basename=True):
    """
    It gets a plain string list with the deleted files from the dvc diff json.

    With only_basename=True
    Input: {"added": [], "deleted": [{"path": "data/000001/32/000001-32.600.2.tif"}], "modified": [], "renamed": []}
    Output: ['000001-32.600.2.tif']

    only_basename=False
    Input: {"added": [], "deleted": [{"path": "data/000001/32/000001-32.600.2.tif"}], "modified": [], "renamed": []}
    Output: ['data/000001/32/000001-32.600.2.tif']
    """
    dvc_diff = DvcDiffParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=True,
        exclude_modified=True,
        exclude_deleted=False,
        exclude_renamed=True,
        only_basename=only_basename,
    )


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


def extract_modified_files_from_dvc_diff(dvc_diff_json, only_basename=True):
    """
    It gets a plain string list with the modified files from the dvc diff json.

    With only_basename=True
    Input: {"added": [], "deleted": [], "modified": [{"path": "data/000001/32/000001-32.600.2.tif"}], "renamed": []}
    Output: ['000001-32.600.2.tif']

    only_basename=False
    Input: {"added": [], "deleted": [], "modified": [{"path": "data/000001/32/000001-32.600.2.tif"}], "renamed": []}
    Output: ['data/000001/32/000001-32.600.2.tif']
    """
    dvc_diff = DvcDiffParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=True,
        exclude_deleted=True,
        exclude_renamed=True,
        only_basename=only_basename,
    )


def extract_renamed_files_from_dvc_diff(dvc_diff_json, only_basename=True):
    """
    It gets a plain string list with the renamed files from the dvc diff json.

    With only_basename=True
    Input: {"added": [], "deleted": [], "modified": [], "renamed": [{"path": {
        "old": "data/000001/32/000001-32.600.2.tif",
        "new": "data/000002/32/000002-32.600.2.tif"
    }}]}
    Output: [
        {
        "old": "data/000001/32/000001-32.600.2.tif",
        "new": "data/000002/32/000002-32.600.2.tif"
        }
    ]

    only_basename=False
    Input: {"added": [], "deleted": [], "modified": [], "renamed": [{"path": {
        "old": "data/000001/32/000001-32.600.2.tif",
        "new": "data/000002/32/000002-32.600.2.tif"
    }}]}
    Output: [
        {
        "old": "000001-32.600.2.tif",
        "new": "000002-32.600.2.tif"
        }
    ]
    """
    dvc_diff = DvcDiffParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=True,
        exclude_modified=True,
        exclude_deleted=True,
        exclude_renamed=False,
        only_basename=only_basename,
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
            {"path": "data/000001/52/000001-52.600.2.tif"},
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


def get_new_filepath_if_is_a_renaming_dict(filepath_or_dict):
    """
    If the parametre is a dict with the "new" key, it will return its value. Otherwise it
    will return the parameter as is.

    This is useful to unify the processing of paths where they are "added/deleted/modified" or
    "renamed"
    """
    if isinstance(filepath_or_dict, dict) and filepath_or_dict["new"]:
        return filepath_or_dict["new"]
    else:
        return filepath_or_dict
