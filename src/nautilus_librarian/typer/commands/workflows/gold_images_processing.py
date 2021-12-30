import typer

from nautilus_librarian.mods.console.domain.utils import get_current_working_directory
from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.mods.git.domain.config import (
    default_git_user_email,
    default_git_user_name,
    default_git_user_signingkey,
)
from nautilus_librarian.mods.git.domain.git_user import GitUser
from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.auto_commit_base_images import (
    auto_commit_base_images,
)
from nautilus_librarian.typer.commands.workflows.actions.dvc_pull_action import (
    dvc_pull_action,
)
from nautilus_librarian.typer.commands.workflows.actions.validate_filenames import (
    validate_filenames,
)
from nautilus_librarian.typer.commands.workflows.actions.validate_filepaths_action import (
    validate_filepaths_action,
)

app = typer.Typer()


def process_action_result(action_result):
    for message in action_result.messages:
        typer.echo(message.text, err=message.is_error)

    if action_result.code is ResultCode.EXIT:
        raise typer.Exit()

    if action_result.code is ResultCode.ABORT:
        raise typer.Abort()


@app.command("gold-images-processing")
def gold_images_processing(
    dvc_diff: str = typer.Argument("{}", envvar="INPUT_DVC_DIFF"),
    git_repo_dir: str = typer.Argument(
        get_current_working_directory, envvar="INPUT_GIT_REPO_DIR"
    ),
    git_user_name: str = typer.Argument(
        default_git_user_name, envvar="INPUT_GIT_USER_NAME"
    ),
    git_user_email: str = typer.Argument(
        default_git_user_email, envvar="INPUT_GIT_USER_EMAIL"
    ),
    git_user_signingkey: str = typer.Argument(
        default_git_user_signingkey, envvar="INPUT_GIT_USER_SIGNINGKEY"
    ),
    dvc_remote: str = typer.Option(
        default=None,
        envvar="NL_DVC_REMOTE",
        help="The name of the DVC remote storage. Use `dvc remote list --project` to get the list of remotes",
    ),
    # Third-party env vars
    gnupghome: str = typer.Argument("~/.gnupg", envvar="GNUPGHOME"),
):
    """
    Gold Images Processing Workflow.

    This workflow process new or updated Gold images in a pull request:

    1. Get new or modified Gold images using dvc diff (TODO).

    2. Pull images from dvc remote storage.

    3. Validate filenames.

    4. Validate filepaths.

    5. Validate image size (TODO).

    6. Generate Base image from Gold (change size and icc profile) (TODO).

    7. Auto-commit new Base images.

    Example:
        poetry run nautilus-librarian gold-images-processing '{"added":[{"path":"data/000001/32/000001-32.600.2.tif"}],"deleted":[],"modified":[],"renamed":[]}' # noqa
    """

    git_user = GitUser(git_user_name, git_user_email, git_user_signingkey)

    process_action_result(validate_filenames(dvc_diff))

    process_action_result(validate_filepaths_action(dvc_diff))

    if dvc_remote is None:
        dvc_remote = DvcApiWrapper(git_repo_dir).dvc_default_remote()

    process_action_result(dvc_pull_action(dvc_diff, git_repo_dir, dvc_remote))

    process_action_result(
        auto_commit_base_images(dvc_diff, git_repo_dir, gnupghome, git_user)
    )


if __name__ == "__main__":
    app()
