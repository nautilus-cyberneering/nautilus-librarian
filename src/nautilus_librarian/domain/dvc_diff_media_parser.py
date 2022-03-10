import json

from nautilus_librarian.mods.dvc.domain.diff.parser import Parser
from nautilus_librarian.mods.namecodes.domain.filename_filters import (
    filter_media_library_files,
)
from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    is_a_library_file,
)


class DvcDiffMediaParser:
    def __init__(self, dvc_diff: dict) -> None:
        self.dvc_diff = dvc_diff
        self.added_list = None
        self.deleted_list = None
        self.modified_list = None
        self.renamed_list = None
        self.dvc_diff_parser = Parser(dvc_diff)

    @staticmethod
    def from_json(dvc_diff):
        return DvcDiffMediaParser(json.loads(dvc_diff))

    def filter(
        self,
        exclude_added=False,
        exclude_deleted=False,
        exclude_modified=False,
        exclude_renamed=False,
        only_basename=False,
    ):
        all_files = []

        if not exclude_added:
            added_list = self.dvc_diff_parser.filter(
                exclude_added=False,
                exclude_deleted=True,
                exclude_modified=True,
                exclude_renamed=True,
                only_basename=only_basename,
            )
            all_files = all_files + filter_media_library_files(added_list)

        if not exclude_deleted:
            deleted_list = self.dvc_diff_parser.filter(
                exclude_added=True,
                exclude_deleted=False,
                exclude_modified=True,
                exclude_renamed=True,
                only_basename=only_basename,
            )
            all_files = all_files + filter_media_library_files(deleted_list)

        if not exclude_modified:
            modified_list = self.dvc_diff_parser.filter(
                exclude_added=True,
                exclude_deleted=True,
                exclude_modified=False,
                exclude_renamed=True,
                only_basename=only_basename,
            )
            all_files = all_files + filter_media_library_files(modified_list)

        if not exclude_renamed:
            renamed_list = self.dvc_diff_parser.filter(
                exclude_added=True,
                exclude_deleted=True,
                exclude_modified=True,
                exclude_renamed=False,
                only_basename=only_basename,
            )
            # It gets only the new name
            new_names_list = list(map(lambda path: path["new"], renamed_list))
            all_files = all_files + filter_media_library_files(new_names_list)

        return all_files


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
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=False,
        exclude_modified=False,
        exclude_deleted=True,
        exclude_renamed=True,
        only_basename=only_basename,
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
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=True,
        exclude_modified=False,
        exclude_deleted=True,
        exclude_renamed=True,
        only_basename=only_basename,
    )


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
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=True,
        exclude_modified=True,
        exclude_deleted=False,
        exclude_renamed=True,
        only_basename=only_basename,
    )


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
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=False,
        exclude_modified=False,
        exclude_deleted=False,
        exclude_renamed=False,
        only_basename=only_basename,
    )


def extract_list_of_new_and_renamed_files_from_dvc_diff_output(dvc_diff_json):
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=False,
        exclude_modified=True,
        exclude_deleted=True,
        exclude_renamed=False,
        only_basename=False,
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
    dvc_diff = Parser.from_json(dvc_diff_json)
    all_files = dvc_diff.filter(
        exclude_added=True,
        exclude_modified=True,
        exclude_deleted=True,
        exclude_renamed=False,
        only_basename=only_basename,
    )

    media_files = list(
        filter(lambda filename: is_a_library_file(filename["new"]), all_files)
    )

    return media_files
