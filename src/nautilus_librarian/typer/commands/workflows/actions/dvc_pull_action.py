from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.mods.dvc.domain.utils import (
    extract_added_and_modified_files_from_dvc_diff,
)
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)


def dvc_pull_action(dvc_diff, git_repo_dir, remote_name):
    """
    It pulls from the dvc remote storage
    all the added or modified library media files in the dvd diff.
    """
    if dvc_diff == "{}":
        return ActionResult(ResultCode.EXIT, [Message("No Gold image changes found")])

    filenames = extract_added_and_modified_files_from_dvc_diff(
        dvc_diff, only_basename=False
    )

    dvcApiWrapper = DvcApiWrapper(git_repo_dir)

    messages = []

    for filename in filenames:
        try:
            # dvc pull --remote azure data/000000/32/000000-32.600.2.tif
            dvcApiWrapper.pull(filename, remote_name)

            messages.append(Message(f"✓ {filename} pulled from dvc storage"))
        except ValueError as error:
            return ActionResult(
                ResultCode.ABORT,
                [
                    ErrorMessage(
                        f"✗ Error pulling the file {filename} from DVC storage. {error}"
                    )
                ],
            )

    return ActionResult(ResultCode.CONTINUE, messages)
