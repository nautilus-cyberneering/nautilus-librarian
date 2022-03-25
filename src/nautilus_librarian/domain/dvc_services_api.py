import os
from os import path
from typing import List

from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.mods.namecodes.domain.media_library_filename import (
    MediaLibraryFilename,
)
from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    is_a_library_file,
)


class InvalidLibraryImage(AssertionError):
    pass


class DvcServicesApi:
    """
    An API wrapping up the DVC API to simplify the interface, enforce
    domain restrictions and conceal internals
    """

    def __init__(self, repo_path):
        self.dvc_api = DvcApiWrapper(repo_path)

    def check_filename_is_library_image(self, filepath):
        if not (
            is_a_library_file(filepath)
            and (
                MediaLibraryFilename(filepath).is_gold_image()
                or MediaLibraryFilename(filepath).is_base_image()
            )
        ):
            raise InvalidLibraryImage(
                f"{filepath} is not a valid library Gold or Base image"
            )

    def check_filename_is_an_existing_library_image(self, filepath):
        absolute_path = filepath
        if not os.path.isabs(filepath):
            # If relative path is provided we use the repo path not the working directory
            absolute_path = f"{self.dvc_api.get_repo_path()}/{filepath}"
        if not path.isfile(absolute_path):
            raise InvalidLibraryImage(
                f"{absolute_path} does not exist. Working dir is: {os.getcwd()}"
            )
        self.check_filename_is_library_image(absolute_path)

    def diff(self, a_rev: str, b_rev: str):
        return self.dvc_api.diff(a_rev, b_rev)

    def add(self, filename: str):
        self.check_filename_is_an_existing_library_image(filename)
        return self.dvc_api.add(filename)

    def push(self, filename: str):
        self.check_filename_is_an_existing_library_image(f"{filename}")
        return self.dvc_api.push(targets=filename)

    def pull(self, filename=None, remote=None):
        if filename is not None:
            self.check_filename_is_library_image(filename)
        return self.dvc_api.pull(targets=filename, remote=remote)

    def remove(self, filename: str):
        self.check_filename_is_an_existing_library_image(filename)
        return self.dvc_api.remove(f"{filename}.dvc")

    def move(self, from_path: str, to_path: str):
        self.check_filename_is_an_existing_library_image(from_path)
        self.check_filename_is_library_image(to_path)
        return self.dvc_api.move(from_path, to_path)

    def dvc_default_remote(self):
        return self.dvc_api.dvc_default_remote()

    def get_files_to_commit(self, base_img_relative_path: str) -> List[str]:
        return self.dvc_api.get_files_to_commit(base_img_relative_path)
