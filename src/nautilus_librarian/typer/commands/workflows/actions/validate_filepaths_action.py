from nautilus_librarian.domain.dvc_diff_media_parser import (
    extract_list_of_new_and_renamed_files_from_dvc_diff_output,
)
from nautilus_librarian.domain.validate_filepaths import validate_filepath
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)


def validate_filepaths_action(dvc_diff):
    """
    It checks the file location for all the media files that have been changed.
    """
    if dvc_diff == "{}":
        return ActionResult(
            ResultCode.EXIT, [Message("No media library file changes found")]
        )

    filepaths = extract_list_of_new_and_renamed_files_from_dvc_diff_output(dvc_diff)

    messages = []

    for filepath in filepaths:
        try:
            validate_filepath(str(filepath))
            messages.append(Message(f"{filepath} ✓"))
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT, [ErrorMessage(f"{filepath} ✗ {error}")]
            )

    return ActionResult(ResultCode.CONTINUE, messages)
