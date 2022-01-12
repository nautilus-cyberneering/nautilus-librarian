from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.mods.dvc.domain.utils import (
    extract_renamed_files_from_dvc_diff,
)
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)

from shutil import move


def get_base_image_absolute_path(git_repo_dir, gold_image):
    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    return f"{git_repo_dir}/{corresponding_base_image_relative_path}"


def rename_base_images(dvc_diff, git_repo_dir):
    """
    It renames previously generated base images when gold images are renamed
    """
    filenames = extract_renamed_files_from_dvc_diff(
        dvc_diff, only_basename=False
    )

    if dvc_diff == "{}" or filenames == []:
        return ActionResult(ResultCode.CONTINUE, [Message("No Gold image renames found")])

    messages = []

    for filename in filenames:
        try:
            gold_filename = Filename(filename)
            base_filename = get_base_image_absolute_path(git_repo_dir, gold_filename)
            move(f"{git_repo_dir}/{filename}", f"{base_filename}")
            messages.append(
                Message(f"✓ Base image of {filename} successfully renamed")
            )
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT,
                [ErrorMessage(f"✗ Error renaming base image of {filename}: {error}")],
            )

    return ActionResult(ResultCode.CONTINUE, messages)
