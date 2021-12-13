import typer

app = typer.Typer()


@app.command("gold-drawings-processing")
def gold_drawings_processing(
    filenames: str = typer.Argument("{}", envvar="INPUT_FILENAMES")
):
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

    if filenames == "{}":
        typer.echo("No Gold image changes found")
        typer.Exit()


if __name__ == "__main__":
    app()
