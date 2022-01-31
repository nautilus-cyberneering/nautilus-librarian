from os import path, remove

from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.mods.dvc.domain.utils import extract_deleted_files_from_dvc_diff
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    Message,
    ResultCode,
)


def get_base_image_absolute_path(git_repo_dir, gold_image):
    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    return f"{git_repo_dir}/{corresponding_base_image_relative_path}"


def remove_base_pointer_and_file_if_exists(base_filename, dvc_api_wrapper):
    dvc_api_wrapper.remove(f"{base_filename}.dvc")
    if path.exists(base_filename):
        remove(base_filename)


def delete_base_images(dvc_diff, git_repo_dir):
    """
    It deletes previously generated base images when gold images are deleted
    """
    filenames = extract_deleted_files_from_dvc_diff(dvc_diff, only_basename=False)

    if dvc_diff == "{}" or filenames == []:
        return ActionResult(
            ResultCode.CONTINUE, [Message("No Gold image deletions found")]
        )

    messages = []
    dvc_api_wrapper = DvcApiWrapper(git_repo_dir)

    for filename in filenames:
        gold_filename = Filename(filename)
        base_filename = get_base_image_absolute_path(git_repo_dir, gold_filename)
        if path.exists(f"{base_filename}.dvc"):
            remove_base_pointer_and_file_if_exists(base_filename, dvc_api_wrapper)
            messages.append(
                Message(f"✓ Base image {base_filename} successfully deleted")
            )

    return ActionResult(ResultCode.CONTINUE, messages)
