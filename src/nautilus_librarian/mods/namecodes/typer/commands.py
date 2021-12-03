import typer

from nautilus_librarian.mods.namecodes.domain.validate_filenames import validate_filename

app = typer.Typer()


@app.command()
def test(echo_string: str):
    """
    It's only used for testing purposes
    """
    typer.echo(f"Testing Namecode module: {echo_string}")


@app.command("validate-filename")
def validate_filename_command(filename: str):
    """
    It checks if a filename follow Nautilus Namecodes conventions (https://github.com/da2ce7/nautilus-namecodes).
    Some filename examples: 000000-32.600.2.tif, 000001-42.600.2.tif.
    """
    validate_filename(filename)

if __name__ == "__main__":
    app()
