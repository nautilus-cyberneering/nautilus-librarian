from nautilus_librarian.mods.dvc.domain.utils import (
    extract_list_of_media_file_changes_from_dvc_diff_output,
    get_new_filepath_if_is_a_renaming_dict,
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


def validate_filenames(dvc_diff):
    """
    It validates all the media file names in the dvc diff.
    """
    if dvc_diff == "{}":
        return ActionResult(ResultCode.EXIT, [Message("No Gold image changes found")])

    filenames = extract_list_of_media_file_changes_from_dvc_diff_output(dvc_diff)

    messages = []

    for filename in filenames:
        try:
            extracted_filename = get_new_filepath_if_is_a_renaming_dict(filename)
            validate_filename(extracted_filename)
            messages.append(Message(f"{extracted_filename} ✓"))
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT, [ErrorMessage(f"{filename} ✗ {error}")]
            )

    return ActionResult(ResultCode.CONTINUE, messages)
