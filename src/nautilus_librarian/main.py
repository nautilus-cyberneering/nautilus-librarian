"""
    Main Module for Librarian
    Usage: main.py [OPTIONS] COMMAND [ARGS]...

    Commands:
      process  Execute the image processing pipeline.
      pull     Retrieves the images from the DVC remote storage.

    Current implementation is just a boilerplate to add logic, now only prints info through console.
"""

import typer
from typer.main import Typer

import nautilus_librarian.mods.dvc.typer.commands
import nautilus_librarian.mods.git.typer.commands
import nautilus_librarian.mods.gpg.typer.commands
import nautilus_librarian.mods.libvips.typer.commands
import nautilus_librarian.mods.namecodes.typer.commands

app: Typer = typer.Typer()


def add_subcommands():
    app.add_typer(nautilus_librarian.mods.dvc.typer.commands.app, name="dvc")
    app.add_typer(nautilus_librarian.mods.git.typer.commands.app, name="git")
    app.add_typer(nautilus_librarian.mods.gpg.typer.commands.app, name="gpg")
    app.add_typer(
        nautilus_librarian.mods.libvips.typer.commands.app, name="libvips")
    app.add_typer(
        nautilus_librarian.mods.namecodes.typer.commands.app, name="namecodes")


@app.command()
def test(echo_string: str):
    typer.echo(f"Testing main module: {echo_string}")


add_subcommands()

if __name__ == "__main__":
    app()
