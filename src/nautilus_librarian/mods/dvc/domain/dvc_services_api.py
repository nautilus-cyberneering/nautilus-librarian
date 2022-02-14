from os import path
from typing import List
from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    is_a_library_file,
)


def check_filename_is_library_image(filepath):
    if not (
        is_a_library_file(filepath)
        and (Filename(filepath).is_gold_image() or Filename(filepath).is_base_image())
    ):
        raise InvalidLibraryImage(
            f"{filepath} is not a valid library Gold or Base image"
        )


def check_filename_is_an_existing_library_image(filepath):
    if not path.isfile(filepath):
        raise InvalidLibraryImage(f"{filepath} does not exist")
    check_filename_is_library_image(filepath)


class InvalidLibraryImage(AssertionError):
    pass


class DvcServicesApi:
    """
    An API wrapping up the DVC API to simplify the interface, enforce
    domain restrictions and conceal internals
    """

    def __init__(self, repo_path):
        self.dvc_api = DvcApiWrapper(repo_path)

    def diff(self, a_rev: str, b_rev: str):
        return self.dvc_api.diff(a_rev, b_rev)

    def add(self, filename: str):
        check_filename_is_an_existing_library_image(filename)
        return self.dvc_api.add(filename)

    def push(self, filename: str):
        check_filename_is_an_existing_library_image(f"{filename}")
        return self.dvc_api.push(targets=filename)

    def pull(self, filename = None, remote = None):
        if filename is not None:
            check_filename_is_library_image(filename)
        return self.dvc_api.pull(targets=filename, remote=remote)

    def remove(self, filename: str):
        check_filename_is_an_existing_library_image(filename)
        return self.dvc_api.remove(f"{filename}.dvc")

    def move(self, from_path: str, to_path: str):
        check_filename_is_an_existing_library_image(from_path)
        check_filename_is_library_image(to_path)
        return self.dvc_api.move(from_path, to_path)

    def get_files_to_commit(self, base_img_relative_path: str) -> List[str]:
        return self.dvc_api.get_files_to_commit(base_img_relative_path)
