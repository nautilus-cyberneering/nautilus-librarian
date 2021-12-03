"""Main Module for Command Line App"""

import typer
from typer.main import Typer

from nautilus_librarian.typer.app import app_init

app: Typer = typer.Typer()

app_init(app)

if __name__ == "__main__":
    app()
