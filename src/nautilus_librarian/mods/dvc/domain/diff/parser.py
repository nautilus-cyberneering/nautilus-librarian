import json
import os


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
        # TODO: refactor. Replace each attribute by a PathList class.
        self.added_list = [element["path"] for element in self.dvc_diff["added"]]
        self.deleted_list = [element["path"] for element in self.dvc_diff["deleted"]]
        self.modified_list = [element["path"] for element in self.dvc_diff["modified"]]
        self.renamed_list = [element["path"] for element in self.dvc_diff["renamed"]]

    def basename_of(self, filepath: str) -> str:
        return os.path.basename(filepath)

    def basenames_of(self, filepaths: list[str]) -> list[str]:
        return [self.basename_of(filepath) for filepath in filepaths]

    def basenames_of_old_and_new(self, filepaths: list[dict]) -> list[dict]:
        return [
            {
                "new": self.basename_of(filepath_dict["new"]),
                "old": self.basename_of(filepath_dict["old"]),
            }
            for filepath_dict in filepaths
        ]

    def added(self, only_basename=False):
        if only_basename:
            return self.basenames_of(self.added_list)

        return self.added_list

    def deleted(self, only_basename=False):
        if only_basename:
            return self.basenames_of(self.deleted_list)

        return self.deleted_list

    def modified(self, only_basename=False):
        if only_basename:
            return self.basenames_of(self.modified_list)

        return self.modified_list

    def renamed(self, only_basename=False):
        if only_basename:
            print("renamed:", self.renamed_list)
            return self.basenames_of_old_and_new(self.renamed_list)

        return self.renamed_list

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
            all_files = all_files + self.added_list

        if not exclude_deleted:
            all_files = all_files + self.deleted_list

        if not exclude_modified:
            all_files = all_files + self.modified_list

        if only_basename:
            all_files = self.basenames_of(all_files)

        if not exclude_renamed:
            if only_basename:
                all_files = all_files + self.basenames_of_old_and_new(self.renamed_list)
            else:
                all_files = all_files + self.renamed_list

        return all_files
