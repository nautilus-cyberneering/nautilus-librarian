"""Main Module for Command Line App"""
from typing import Optional

import typer
from typer.main import Typer

from nautilus_librarian._version import __version__
from nautilus_librarian.typer.app import app_init

app: Typer = typer.Typer()


def version_callback(value: bool) -> None:
    """Simple Callback Function to return the Version Number of the Program"""

    if value:
        typer.echo(f"Librarian Version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(  # pylint: disable=unused-argument
        None, "--version", callback=version_callback
    ),
):
    """Main Function of CLI application, defining main options."""
    return


app_init(app)

if __name__ == "__main__":
    app()
