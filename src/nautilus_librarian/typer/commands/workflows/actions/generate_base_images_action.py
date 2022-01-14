from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.mods.dvc.domain.utils import (
    extract_added_and_modified_files_from_dvc_diff,
)
from nautilus_librarian.mods.libvips.domain.process_image import process_image
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)


def get_base_image_absolute_path(git_repo_dir, gold_image):
    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    return f"{git_repo_dir}/{corresponding_base_image_relative_path}"


def generate_base_images(dvc_diff, git_repo_dir, base_images_size):
    """
    It generates the base images of all the media sizes in the dvc diff.
    """
    filenames = extract_added_and_modified_files_from_dvc_diff(
        dvc_diff, only_basename=False
    )

    if dvc_diff == "{}" or filenames == []:
        return ActionResult(ResultCode.EXIT, [Message("No Gold image changes found")])

    messages = []

    for filename in filenames:
        try:
            gold_filename = Filename(filename)
            base_filename = get_base_image_absolute_path(git_repo_dir, gold_filename)
            process_image(
                f"{git_repo_dir}/{filename}", f"{base_filename}", base_images_size
            )
            messages.append(
                Message(f"✓ Base image of {filename} successfully generated")
            )
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT,
                [ErrorMessage(f"✗ Error generating base image of {filename}: {error}")],
            )

    return ActionResult(ResultCode.CONTINUE, messages)
