import typer
from typer.main import Typer

import nautilus_librarian.typer.commands
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
    app.add_typer(nautilus_librarian.mods.libvips.typer.commands.app, name="libvips")
    app.add_typer(
        nautilus_librarian.mods.namecodes.typer.commands.app, name="namecodes"
    )


def app_init():
    add_subcommands()
    return app
