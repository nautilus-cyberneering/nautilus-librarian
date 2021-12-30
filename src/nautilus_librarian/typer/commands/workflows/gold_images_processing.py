import typer

from nautilus_librarian.mods.console.domain.utils import get_current_working_directory
from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.mods.git.domain.config import git_config_global_user
from nautilus_librarian.mods.git.domain.git_user import GitUser
from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.auto_commit_base_images import (
    auto_commit_base_images,
)
from nautilus_librarian.typer.commands.workflows.actions.validate_filenames import (
    validate_filenames,
)

app = typer.Typer()


def process_action_result(action_result):
    for message in action_result.messages:
        typer.echo(message.text, err=message.is_error)

    if action_result.code is ResultCode.EXIT:
        raise typer.Exit()

    if action_result.code is ResultCode.ABORT:
        raise typer.Abort()


def default_git_user_name():
    git_config_global_user().name


def default_git_user_email():
    git_config_global_user().email


def default_git_user_signingkey():
    git_config_global_user().signingkey


def get_dvc_diff_if_not_provided(dvc_diff, repo_dir):
    if not dvc_diff:
        return str(DvcApiWrapper(repo_dir).diff()).replace("'", '"')
    else:
        return dvc_diff


@app.command("gold-images-processing")
def gold_images_processing(
    git_user_name: str = typer.Argument(
        default_git_user_name, envvar="NL_GIT_USER_NAME"
    ),
    git_user_email: str = typer.Argument(
        default_git_user_email, envvar="NL_GIT_USER_EMAIL"
    ),
    git_user_signingkey: str = typer.Argument(
        default_git_user_signingkey, envvar="NL_GIT_USER_SIGNINGKEY"
    ),
    git_repo_dir: str = typer.Option(
        get_current_working_directory, envvar="NL_GIT_REPO_DIR"
    ),
    dvc_diff: str = typer.Option(None, envvar="NL_DVC_DIFF"),
    # Third-party env vars
    gnupghome: str = typer.Argument("~/.gnupg", envvar="GNUPGHOME"),
):
    """
    Gold Images Processing Workflow.

    This workflow process new or updated Gold images in a pull request:

    1. Get new or modified Gold images using dvc diff (TODO).

    2. Pull images from dvc remote storage (TODO).

    3. Validate filenames.

    4. Validate filepaths (TODO).

    5. Validate image size (TODO).

    6. Generate Base image from Gold (change size and icc profile) (TODO).

    7. Auto-commit new Base images.

    Example:
        poetry run nautilus-librarian gold-images-processing /path/to/repo '{"added":[{"path":"data/000001/32/000001-32.600.2.tif"}],"deleted":[],"modified":[],"renamed":[]}' # noqa
    """

    git_user = GitUser(git_user_name, git_user_email, git_user_signingkey)

    dvc_diff = get_dvc_diff_if_not_provided(None, git_repo_dir)

    process_action_result(validate_filenames(dvc_diff))

    process_action_result(
        auto_commit_base_images(dvc_diff, git_repo_dir, gnupghome, git_user)
    )


if __name__ == "__main__":
    app()
