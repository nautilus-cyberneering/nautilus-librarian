import json

from nautilus_librarian.mods.dvc.domain.diff.path_list import PathList


class Parser:
    def __init__(self, dvc_diff: dict) -> None:
        self.dvc_diff = dvc_diff
        self.added_list = None
        self.deleted_list = None
        self.modified_list = None
        self.renamed_list = None

        self.parse()

    @staticmethod
    def from_json(dvc_diff):
        return Parser(json.loads(dvc_diff))

    def parse(self):
        self.added_list = PathList.from_dict_list(self.dvc_diff["added"])
        self.deleted_list = PathList.from_dict_list(self.dvc_diff["deleted"])
        self.modified_list = PathList.from_dict_list(self.dvc_diff["modified"])
        self.renamed_list = PathList.from_dict_list(self.dvc_diff["renamed"])

    def filter(
        self,
        exclude_added=False,
        exclude_deleted=False,
        exclude_modified=False,
        exclude_renamed=False,
    ) -> PathList:
        all_files = PathList([])

        if not exclude_added:
            all_files = all_files + self.added_list

        if not exclude_deleted:
            all_files = all_files + self.deleted_list

        if not exclude_modified:
            all_files = all_files + self.modified_list

        if not exclude_renamed:
            all_files = all_files + self.renamed_list

        return all_files
