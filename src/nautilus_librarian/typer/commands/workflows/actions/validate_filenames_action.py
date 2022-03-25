from nautilus_librarian.mods.dvc.domain.utils import (
    extract_all_added_and_renamed_files_from_dvc_diff,
)
from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    validate_filename,
)
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)


def validate_filenames_action(dvc_diff):
    """
    It validates all the filenames in the dvc diff.
    """
    if dvc_diff == "{}":
        return ActionResult(
            ResultCode.EXIT, [Message("No filenames to validate, empty DVC diff")]
        )

    # TODO: we have to review this function if we add files to DVC which do not belong to a media library.

    filenames = extract_all_added_and_renamed_files_from_dvc_diff(dvc_diff)

    messages = []

    for filename in filenames:
        try:
            validate_filename(str(filename))
            messages.append(Message(f"{filename} ✓"))
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT, [ErrorMessage(f"{filename} ✗ {error}")]
            )

    return ActionResult(ResultCode.CONTINUE, messages)
