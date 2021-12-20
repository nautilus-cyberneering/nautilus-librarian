import os
from typing import List

from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.mods.dvc.domain.utils import (
    dvc_add,
    dvc_push,
    extract_added_files_from_dvc_diff,
)
from nautilus_librarian.mods.git.domain.config import git_config_global_user
from nautilus_librarian.mods.git.domain.repo import GitRepo
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.mods.namecodes.domain.filename_filters import filter_gold_images


class FileNotFoundException(Exception):
    """Raised when an expected file is not found"""

    pass


def get_new_gold_images_filenames_from_dvc_diff(dvc_diff) -> List[Filename]:
    """
    Parses the list of added Gold images from dvc diff output in json format
    and returns a list of Filenames.
    """
    added_files = extract_added_files_from_dvc_diff(dvc_diff)
    gold_images = filter_gold_images(added_files)
    return [Filename(gold_image) for gold_image in gold_images]


def guard_that_base_image_exists(base_image_path):
    if not os.path.isfile(base_image_path):
        raise FileNotFoundException(f"Missing Base image: {base_image_path}")


def files_to_commit(base_img_relative_path) -> List[str]:
    """
    Given the relative path of a Base image it returns the relative paths
    of the files we have to include in the git repo.

    For example:

    For the Base image "data/000001/42/000001-42.600.2.tif", these are
    the files tracked on the git repo:

    - data/000001/42/.gitignore
    - data/000001/42/000001-42.600.2.tif.dvc
    """
    base_img_dir = os.path.dirname(base_img_relative_path)

    filepaths = [
        f"{base_img_dir}/.gitignore",
        f"{base_img_relative_path}.dvc",
    ]

    return filepaths


def commit_base_image(git_repo_dir, base_img_relative_path):
    git_global_user = git_config_global_user()

    repo = GitRepo(git_repo_dir, git_global_user)

    return repo.commit(
        files_to_commit(base_img_relative_path),
        commit_message=f"feat: new base image: {os.path.basename(base_img_relative_path)}",
    )


def calculate_the_corresponding_base_image_from_gold_image(git_repo_dir, gold_image):
    """
    Returns the Base image path which correspond to the given Gold image.

    Code Review: LibraryFilePath class? and rename Filename to LibraryFilename?
    """
    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    corresponding_base_image_absolute_path = (
        git_repo_dir + "/" + corresponding_base_image_relative_path
    )
    return (
        corresponding_base_image_relative_path,
        corresponding_base_image_absolute_path,
    )


def auto_commit_base_images(typer, dvc_diff, git_repo_dir):
    """
    Workflow step: auto-commit new Base images generated during the workflow execution
    in previous steps.

    TODO:
    Case 1. Added Gold images.
    For each added Gold image:
      [✓] 1. Calculate the corresponding Base image filename and filepath.
      [✓] 2. Check if the Base image exists.
      [✓] 3. Add the image to dvc.
      [✓] 4. Push the image to remote dvc storage.
      [✓] 5. Commit the image to the current branch with a signed commit.

    Points 2 to 5 are different depending on whether we are adding,
    modifying or renaming the Gold image.

    Case 2. Modified Gold images.
    For each modified Gold image:
      [ ] 1. ??
      [ ] 2. ...
      [ ] 3. ??
    Pending to define:
    https://github.com/Nautilus-Cyberneering/chinese-ideographs/pull/122#issuecomment-972844365

    Case 3. Renamed Gold images.
    For each renamed Gold image:
      [ ] 1. ??
      [ ] 2. ...
      [ ] 3. ??
    Pending to define:
    https://github.com/Nautilus-Cyberneering/chinese-ideographs/pull/122#issuecomment-972844365
    """
    gold_images = get_new_gold_images_filenames_from_dvc_diff(dvc_diff)

    for gold_image in gold_images:
        (
            base_img_relative_path,
            base_img_absolute_path,
        ) = calculate_the_corresponding_base_image_from_gold_image(
            git_repo_dir, gold_image
        )

        # TODO: inject console_printer to remove dependency with typer so that we can create
        # unit tests for workflow steps.
        typer.echo(
            f"New Gold image found: {gold_image} -> Base image: {base_img_relative_path} ✓ "
        )

        guard_that_base_image_exists(base_img_absolute_path)
        dvc_add(base_img_relative_path, git_repo_dir)
        dvc_push(f"{base_img_relative_path}.dvc", git_repo_dir)

        commit_base_image(git_repo_dir, base_img_relative_path)
