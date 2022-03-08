from os import path, remove

from nautilus_librarian.domain.dvc_diff_media_parser import (
    extract_deleted_files_from_dvc_diff,
)
from nautilus_librarian.domain.dvc_services_api import DvcServicesApi
from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.mods.namecodes.domain.media_library_filename import (
    MediaLibraryFilename,
)
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    Message,
    ResultCode,
)


def get_base_image_absolute_path_from_gold(git_repo_dir, gold_image):
    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    return f"{git_repo_dir}/{corresponding_base_image_relative_path}"


def remove_base_pointer_and_file_if_exists(base_filename, dvc_services):
    dvc_services.remove(base_filename)
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
    dvc_services = DvcServicesApi(git_repo_dir)

    for filename in filenames:
        gold_filename = MediaLibraryFilename(filename)
        base_filename = get_base_image_absolute_path_from_gold(
            git_repo_dir, gold_filename
        )
        if path.exists(f"{base_filename}.dvc"):
            remove_base_pointer_and_file_if_exists(base_filename, dvc_services)
            messages.append(
                Message(f"✓ Base image {base_filename} successfully deleted")
            )

    return ActionResult(ResultCode.CONTINUE, messages)
