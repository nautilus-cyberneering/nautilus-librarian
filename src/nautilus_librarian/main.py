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
from enum import Enum


app: Typer = typer.Typer()


class Step(Enum):
    validate_size = "validate_size"
    resize = "resize"
    modify_icc_profile = "modify_icc_profile"


def validate_size():
    print("- Validating size of the images")


def resize():
    print("- Resizing images")


def icc_modify():
    print("- Modifying ICC color profiles")


stepExecuters = {
    'validate_size': validate_size,
    'resize': resize,
    'modify_icc_profile': icc_modify
}


def execute_pipeline():
    validate_size()
    resize()
    icc_modify()


@app.command()
def process(step: Step = None):
    """
    Execute the image processing pipeline.

    If --step is used, only specified step is executed.
    """
    if not step:
        execute_pipeline()
    else:
        typer.echo(f"Processing images, using step {step}")
        stepExecuters[step.value]()


@app.command()
def pull():
    """
    Retrieves the images from the DVC remote storage.
    """
    typer.echo(f"Importing images from DVC storage")


if __name__ == "__main__":
    app()
