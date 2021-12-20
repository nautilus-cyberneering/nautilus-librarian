import typer

from nautilus_librarian.mods.console.domain.utils import get_current_working_directory
from nautilus_librarian.typer.commands.workflows.actions.auto_commit_base_images import (
    auto_commit_base_images,
)
from nautilus_librarian.typer.commands.workflows.actions.validate_filenames import (
    validate_filenames,
)

app = typer.Typer()


@app.command("gold-drawings-processing")
def gold_drawings_processing(
    dvc_diff: str = typer.Argument("{}", envvar="INPUT_DVC_DIFF"),
    git_repo_dir: str = typer.Argument(
        get_current_working_directory, envvar="INPUT_GIT_REPO_DIR"
    ),
):
    """
    Gold Drawings Processing Workflow.

    This workflow process new or updated Gold images in a pull request:

    1. Get new or modified Gold images using dvc diff (TODO).

    2. Pull images from dvc remote storage (TODO).

    3. Validate filenames.

    4. Validate filepaths (TODO).

    5. Validate image size (TODO).

    6. Generate Base image from Gold (change size and icc profile) (TODO).

    7. Auto-commit new Base images (TODO).

    Example:
        poetry run nautilus-librarian gold-drawings-processing '{"added":[{"path":"data/000001/32/000001-32.600.2.tif"}],"deleted":[],"modified":[],"renamed":[]}' # noqa
    """

    validate_filenames(typer, dvc_diff)
    auto_commit_base_images(typer, dvc_diff, git_repo_dir)


if __name__ == "__main__":
    app()
