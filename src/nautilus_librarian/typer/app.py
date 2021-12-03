import nautilus_librarian.mods.dvc.typer.commands
import nautilus_librarian.mods.git.typer.commands
import nautilus_librarian.mods.gpg.typer.commands
import nautilus_librarian.mods.libvips.typer.commands
import nautilus_librarian.mods.namecodes.typer.commands
import nautilus_librarian.typer.commands


def add_commands(app):
    app.command()(nautilus_librarian.typer.commands.test)


def add_subcommands(app):
    app.add_typer(nautilus_librarian.mods.dvc.typer.commands.app, name="dvc")
    app.add_typer(nautilus_librarian.mods.git.typer.commands.app, name="git")
    app.add_typer(nautilus_librarian.mods.gpg.typer.commands.app, name="gpg")
    app.add_typer(nautilus_librarian.mods.libvips.typer.commands.app, name="libvips")
    app.add_typer(
        nautilus_librarian.mods.namecodes.typer.commands.app, name="namecodes"
    )


def app_init(app):
    add_commands(app)
    add_subcommands(app)
