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
from nautilus_librarian.typer.commands.workflows.actions.check_images_changes import (
    check_images_changes,
)
from nautilus_librarian.typer.commands.workflows.actions.delete_base_images_action import (
    delete_base_images,
)
from nautilus_librarian.typer.commands.workflows.actions.dvc_pull_action import (
    dvc_pull_action,
)
from nautilus_librarian.typer.commands.workflows.actions.generate_base_images_action import (
    generate_base_images,
)
from nautilus_librarian.typer.commands.workflows.actions.rename_base_images_action import (
    rename_base_images,
)
from nautilus_librarian.typer.commands.workflows.actions.validate_filenames import (
    validate_filenames,
)
from nautilus_librarian.typer.commands.workflows.actions.validate_filepaths_action import (
    validate_filepaths_action,
)
from nautilus_librarian.typer.commands.workflows.actions.validate_images_dimensions_action import (
    validate_images_dimensions,
)

app = typer.Typer()


def process_action_result(action_result):
    for message in action_result.messages:
        typer.echo(message.text, err=message.is_error)

    if action_result.code is ResultCode.EXIT:
        raise typer.Exit()

    if action_result.code is ResultCode.ABORT:
        raise typer.Abort()


def get_dvc_diff_if_not_provided(dvc_diff, repo_dir, previous_ref, current_ref):
    if not dvc_diff:
        return str(
            DvcApiWrapper(repo_dir).diff(a_rev=previous_ref, b_rev=current_ref)
        ).replace("'", '"')
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
    min_image_size: int = typer.Option(256, envvar="NL_MIN_IMAGE_SIZE"),
    max_image_size: int = typer.Option(16384, envvar="NL_MAX_IMAGE_SIZE"),
    base_image_size: int = typer.Option(512, envvar="NL_BASE_IMAGE_SIZE"),
    dvc_diff: str = typer.Option(None, envvar="NL_DVC_DIFF"),
    previous_ref: str = typer.Option("HEAD", envvar="NL_PREVIOUS_REF"),
    current_ref: str = typer.Option(None, envvar="NL_CURRENT_REF"),
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
        poetry run nautilus-librarian gold-images-processing /path/to/repo '{"added":[{"path":"data/000001/32/000001-32.600.2.tif"}],"deleted":[],"modified":[],"renamed":[]}' # noqa
    """

    git_user = GitUser(git_user_name, git_user_email, git_user_signingkey)

    dvc_diff = get_dvc_diff_if_not_provided(
        None, git_repo_dir, previous_ref, current_ref
    )

    process_action_result(validate_filenames(dvc_diff))

    process_action_result(validate_filepaths_action(dvc_diff))

    if dvc_remote is None:
        dvc_remote = DvcApiWrapper(git_repo_dir).dvc_default_remote()

    process_action_result(dvc_pull_action(dvc_diff, git_repo_dir, dvc_remote))

    process_action_result(check_images_changes(dvc_diff))

    process_action_result(
        validate_images_dimensions(dvc_diff, min_image_size, max_image_size)
    )

    process_action_result(generate_base_images(dvc_diff, git_repo_dir, base_image_size))

    process_action_result(rename_base_images(dvc_diff, git_repo_dir))

    process_action_result(delete_base_images(dvc_diff, git_repo_dir))

    process_action_result(
        auto_commit_base_images(dvc_diff, git_repo_dir, gnupghome, git_user)
    )


if __name__ == "__main__":
    app()
