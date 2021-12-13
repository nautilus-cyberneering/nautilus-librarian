import typer

from nautilus_librarian.mods.dvc.domain.utils import (
    extract_modified_media_file_list_from_dvd_diff_output,
)
from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    validate_filename,
)

app = typer.Typer()


@app.command("gold-drawings-processing")
def gold_drawings_processing(dvc_diff: str = typer.Argument("{}", envvar="INPUT_DIFF")):
    """
    Gold Drawings Processing Workflow.

    This workflow process new or updated Gold images in a pull request:

    1. Get new or modified Gold images using dvc diff (TODO).

    2. Pull images from dvc remote storage (TODO).

    3. Validate filenames and filepaths.

    4. Validate image size (TODO).

    5. Generate Base image from Gold (change size and icc profile) (TODO).

    6. Auto-commit new Base images (TODO).
    """

    if dvc_diff == "{}":
        typer.echo("No Gold image changes found")
        raise typer.Exit()

    filenames = extract_modified_media_file_list_from_dvd_diff_output(dvc_diff)

    for filename in filenames:
        try:
            validate_filename(filename)
            typer.echo(f"{filename} ✓")
        except ValueError as error:
            typer.echo(f"{filename} ✗ {error}", err=True)
            raise typer.Abort()


if __name__ == "__main__":
    app()
