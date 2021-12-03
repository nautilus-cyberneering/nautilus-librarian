import typer

from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    validate_filename,
)

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
    Validate filename with Nautilus Namecodes Specification.

    More information about the specification on: https://github.com/da2ce7/nautilus-namecodes.

    Filename examples: 000000-32.600.2.tif, 000001-42.600.2.tif.

    EXAMPLES:

        nautilus-librarian namecodes validate-filename 000000-32.600.2.tif

        A valid filename will show nothing.

        nautilus-librarian namecodes validate-filename 00000032.600.2.tif

        An invalid filename will throw an exception.
    """
    validate_filename(filename)


if __name__ == "__main__":
    app()
