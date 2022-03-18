from nautilus_librarian.domain.dvc_diff_media_parser import (
    extract_added_and_modified_files_from_dvc_diff,
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


def validate_images_dimensions_action(
    dvc_diff, git_repo_dir, min_image_size, max_image_size
):
    """
    It validates all the media sizes in the dvc diff.
    """
    if dvc_diff == "{}":
        return ActionResult(
            ResultCode.CONTINUE, [Message("No Gold image changes found")]
        )

    filenames = extract_added_and_modified_files_from_dvc_diff(dvc_diff)

    messages = []

    for filename in filenames:
        absolute_filepath = f"{git_repo_dir}/{filename}"
        try:
            (width, height) = validate_image_dimensions(
                absolute_filepath, min_image_size, max_image_size
            )
            messages.append(
                Message(f"✓ Dimensions of {str(filename)} are {width} x {height}")
            )
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT,
                [ErrorMessage(f"✗ Dimensions of {str(filename)} are wrong: {error}")],
            )

    return ActionResult(ResultCode.CONTINUE, messages)
