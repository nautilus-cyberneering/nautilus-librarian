from nautilus_librarian.domain.file_locator import file_locator
from nautilus_librarian.mods.dvc.domain.utils import (
    extract_list_of_media_file_changes_from_dvc_diff_output,
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
    if dvc_diff == "{}":
        return ActionResult(ResultCode.EXIT, [Message("No Gold image changes found")])

    filenames = extract_list_of_media_file_changes_from_dvc_diff_output(
        dvc_diff, only_basename=False
    )

    messages = []

    for filename in filenames:
        try:
            gold_filename = Filename(filename)
            base_filename = get_base_image_absolute_path(git_repo_dir, gold_filename)
            process_image(f"{filename}", f"{base_filename}", base_images_size)
            messages.append(
                Message(f"✓ Base image of {filename} successfully generated")
            )
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT,
                [ErrorMessage(f"✗ Error generating base image of {filename}: {error}")],
            )

    return ActionResult(ResultCode.CONTINUE, messages)
