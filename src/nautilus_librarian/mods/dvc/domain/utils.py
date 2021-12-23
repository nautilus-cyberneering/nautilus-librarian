import json
import os

from nautilus_librarian.mods.console.domain.utils import execute_console_command


def extract_basenames_from_filepaths(filepaths):
    return [os.path.basename(filename) for filename in filepaths]


def extract_added_and_modified_and_renamed_files_from_dvc_diff(dvc_diff):
    """
    It gets a plain string list with the added, modified or renamed files from the dvc diff json.
    Input: {"added": [{"path": "data/000001/32/000001-32.600.2.tif"}], "deleted": [], "modified": [], "renamed": []}
    Output: ['data/000001/32/000001-32.600.2.tif']
    """

    data = json.loads(dvc_diff)

    filenames = data["added"] + data["modified"] + data["renamed"]

    # Extract filepaths
    filepaths = [path_object["path"] for path_object in filenames]

    return filepaths


def extract_modified_media_file_list_from_dvd_diff_output(dvc_diff):
    filepaths = extract_added_and_modified_and_renamed_files_from_dvc_diff(dvc_diff)
    filenames = extract_basenames_from_filepaths(filepaths)
    return filenames


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
