from os import makedirs, path
from shutil import move

from nautilus_librarian.domain.file_locator import (
    file_locator,
    guard_that_base_image_exists,
)
from nautilus_librarian.mods.dvc.domain.utils import extract_renamed_files_from_dvc_diff
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)


class BaseImageNotFoundError(FileNotFoundError):
    """Raised when the base image that is to be deleted does not exist"""

    pass


def get_base_image_absolute_path(git_repo_dir, gold_image):
    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    return f"{git_repo_dir}/{corresponding_base_image_relative_path}"


def create_output_folder(destination_filename):
    makedirs(path.dirname(destination_filename), exist_ok=True)


def rename_base_images(dvc_diff, git_repo_dir):
    """
    It renames previously generated base images when gold images are renamed
    """
    filenames = extract_renamed_files_from_dvc_diff(dvc_diff, only_basename=False)

    if dvc_diff == "{}" or filenames == []:
        return ActionResult(ResultCode.EXIT, [Message("No Gold image renames found")])

    messages = []

    for filename in filenames:
        try:
            gold_filename_old = Filename(filename["old"])
            gold_filename_new = Filename(filename["new"])
            base_filename_old = get_base_image_absolute_path(
                git_repo_dir, gold_filename_old
            )
            base_filename_new = get_base_image_absolute_path(
                git_repo_dir, gold_filename_new
            )
            guard_that_base_image_exists(base_filename_old)
            create_output_folder(base_filename_new)
            move(f"{base_filename_old}", f"{base_filename_new}")
            messages.append(
                Message(
                    f"✓ Base image {base_filename_old} successfully renamed to {base_filename_new}"
                )
            )
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT,
                [
                    ErrorMessage(
                        f"✗ Error renaming base image of {gold_filename_new}: {error}"
                    )
                ],
            )

    return ActionResult(ResultCode.CONTINUE, messages)
