from os import makedirs, path

from nautilus_librarian.domain.dvc_diff_media_parser import (
    extract_renamed_files_from_dvc_diff,
)
from nautilus_librarian.domain.dvc_services_api import DvcServicesApi
from nautilus_librarian.domain.file_locator import (
    get_base_image_absolute_path_from_gold,
    guard_that_base_image_exists,
)
from nautilus_librarian.mods.namecodes.domain.media_library_filename import (
    MediaLibraryFilename,
)
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)


def create_output_folder(destination_filename):
    makedirs(path.dirname(destination_filename), exist_ok=True)


def rename_base_images(dvc_diff, git_repo_dir):
    """
    It renames previously generated base images when gold images are renamed
    """
    all_renamed_files = extract_renamed_files_from_dvc_diff(
        dvc_diff, only_basename=False
    )

    # Filter Gold renamed images
    gold_renamed_images = list(
        filter(
            lambda filename: MediaLibraryFilename(filename["old"]).is_gold_image(),
            all_renamed_files,
        )
    )

    if dvc_diff == "{}" or gold_renamed_images == []:
        return ActionResult(
            ResultCode.CONTINUE, [Message("No Gold renamed images found")]
        )

    messages = []

    for filename in gold_renamed_images:
        try:
            gold_filename_old = MediaLibraryFilename(filename["old"])
            base_filename_old = get_base_image_absolute_path_from_gold(
                git_repo_dir, gold_filename_old
            )
            gold_filename_new = MediaLibraryFilename(filename["new"])
            base_filename_new = get_base_image_absolute_path_from_gold(
                git_repo_dir, gold_filename_new
            )
            guard_that_base_image_exists(base_filename_old)
            create_output_folder(base_filename_new)
            dvc_services = DvcServicesApi(git_repo_dir)
            dvc_services.move(f"{base_filename_old}", f"{base_filename_new}")
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
