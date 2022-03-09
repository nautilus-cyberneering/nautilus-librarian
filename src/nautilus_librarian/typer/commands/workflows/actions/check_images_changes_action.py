from nautilus_librarian.domain.dvc_diff_media_parser import (
    extract_all_changed_files_from_dvc_diff,
)
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    Message,
    ResultCode,
)


def check_images_changes_action(dvc_diff):
    """
    It checks for any image changes (add/modify/delete/rename).
    """

    if dvc_diff == "{}" or extract_all_changed_files_from_dvc_diff(dvc_diff) == []:
        return ActionResult(ResultCode.EXIT, [Message("No Gold image changes found")])

    return ActionResult(ResultCode.CONTINUE, [])
