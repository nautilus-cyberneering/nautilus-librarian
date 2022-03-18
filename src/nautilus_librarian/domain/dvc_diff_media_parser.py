import json

from nautilus_librarian.mods.dvc.domain.diff.parser import Parser
from nautilus_librarian.mods.dvc.domain.diff.path import Path
from nautilus_librarian.mods.dvc.domain.diff.path_list import PathList
from nautilus_librarian.mods.namecodes.domain.filename_filters import (
    filter_media_library_files,
)
from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    is_a_library_file,
)


def filter_media_library_paths(path: Path):
    return is_a_library_file(str(path))


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
    ) -> PathList:
        all_files = PathList([])

        if not exclude_added:
            added_list = self.dvc_diff_parser.filter(
                exclude_added=False,
                exclude_deleted=True,
                exclude_modified=True,
                exclude_renamed=True,
            )
            all_files = all_files + PathList.from_string_list(
                filter_media_library_files(added_list.as_plain_list())
            )

        if not exclude_deleted:
            deleted_list = self.dvc_diff_parser.filter(
                exclude_added=True,
                exclude_deleted=False,
                exclude_modified=True,
                exclude_renamed=True,
            )
            all_files = all_files + PathList.from_string_list(
                filter_media_library_files(deleted_list.as_plain_list())
            )

        if not exclude_modified:
            modified_list = self.dvc_diff_parser.filter(
                exclude_added=True,
                exclude_deleted=True,
                exclude_modified=False,
                exclude_renamed=True,
            )
            all_files = all_files + PathList.from_string_list(
                filter_media_library_files(modified_list.as_plain_list())
            )

        if not exclude_renamed:
            renamed_list = self.dvc_diff_parser.filter(
                exclude_added=True,
                exclude_deleted=True,
                exclude_modified=True,
                exclude_renamed=False,
            )
            all_files = all_files + renamed_list.filter(filter_media_library_paths)

        return all_files


def extract_added_and_modified_files_from_dvc_diff(dvc_diff_json) -> list[str]:
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=False,
        exclude_modified=False,
        exclude_deleted=True,
        exclude_renamed=True,
    ).as_plain_list()


def extract_modified_files_from_dvc_diff(dvc_diff_json) -> list[str]:
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=True,
        exclude_modified=False,
        exclude_deleted=True,
        exclude_renamed=True,
    ).as_plain_list()


def extract_deleted_files_from_dvc_diff(dvc_diff_json) -> list[str]:
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=True,
        exclude_modified=True,
        exclude_deleted=False,
        exclude_renamed=True,
    ).as_plain_list()


def extract_all_changed_files_from_dvc_diff(dvc_diff_json) -> list[str]:
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=False,
        exclude_modified=False,
        exclude_deleted=False,
        exclude_renamed=False,
    ).as_plain_list()


def extract_list_of_new_and_renamed_files_from_dvc_diff_output(
    dvc_diff_json,
) -> PathList:
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=False,
        exclude_modified=True,
        exclude_deleted=True,
        exclude_renamed=False,
    )


def extract_renamed_files_from_dvc_diff(dvc_diff_json) -> PathList:
    dvc_diff = DvcDiffMediaParser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_added=True,
        exclude_modified=True,
        exclude_deleted=True,
        exclude_renamed=False,
    )
