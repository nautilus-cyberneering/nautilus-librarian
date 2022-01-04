from nautilus_librarian.mods.dvc.domain.utils import (
    extract_list_of_media_file_changes_from_dvc_diff_output,
)
from nautilus_librarian.mods.libvips.domain.validate_image_dimensions import (
    validate_image_dimensions,
)
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)


def validate_images_dimensions(dvc_diff, min_image_size, max_image_size):
    """
    It validates all the media sizes in the dvc diff.
    """
    if dvc_diff == "{}":
        return ActionResult(ResultCode.EXIT, [Message("No Gold image changes found")])

    filenames = extract_list_of_media_file_changes_from_dvc_diff_output(
        dvc_diff, only_basename=False
    )

    messages = []

    for filename in filenames:
        try:
            (width, height) = validate_image_dimensions(
                filename, min_image_size, max_image_size
            )
            messages.append(
                Message(f"Dimensions of {filename} are {width} x {height} ✓")
            )
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT,
                [ErrorMessage(f"✗ Error validating {filename} dimensions: {error}")],
            )

    return ActionResult(ResultCode.CONTINUE, messages)
