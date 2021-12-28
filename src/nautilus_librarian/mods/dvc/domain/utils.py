import json
import os

from nautilus_librarian.mods.console.domain.utils import execute_console_command


def extract_basename_from_filepath(filepath: str) -> str:
    return os.path.basename(filepath)


def extract_basenames_from_filepaths(filepaths: list[str]) -> list[str]:
    return [extract_basename_from_filepath(filepath) for filepath in filepaths]


def extract_added_and_modified_and_renamed_files_from_dvc_diff(
    dvc_diff, only_basename=True
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

    data = json.loads(dvc_diff)

    filepath_objects = data["added"] + data["modified"] + data["renamed"]
    filepaths = [path_object["path"] for path_object in filepath_objects]

    if only_basename:
        filepaths = extract_basenames_from_filepaths(filepaths)

    return filepaths


def extract_list_of_media_file_changes_from_dvd_diff_output(
    dvc_diff, only_basename=True
):
    return extract_added_and_modified_and_renamed_files_from_dvc_diff(
        dvc_diff, only_basename
    )


def extract_added_files_from_dvc_diff(dvc_diff):
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

    TODO: we should use the dvc API wrapper.
    """
    data = json.loads(dvc_diff)
    return [(path_object["path"]) for path_object in data["added"]]


def dvc_add(filepath, git_repo_dir):
    """
    Wrapper for dvc add command.

    TODO: replace by API wrapper once API wrapper is merged.
    https://github.com/Nautilus-Cyberneering/nautilus-librarian/pull/25
    """
    return execute_console_command(f"dvc add {filepath}", cwd=git_repo_dir)


def dvc_push(filepath, git_repo_dir):
    """
    Wrapper for dvc push command.

    TODO: replace by API wrapper once API wrapper is merged.
    https://github.com/Nautilus-Cyberneering/nautilus-librarian/pull/25
    """
    return execute_console_command(f"dvc push {filepath}", cwd=git_repo_dir)
