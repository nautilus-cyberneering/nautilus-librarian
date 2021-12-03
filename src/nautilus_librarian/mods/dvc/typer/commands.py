import typer

app = typer.Typer()


@app.command()
def test(echo_string: str):
    """
    It's only used for testing purposes
    """
    typer.echo(f"Testing DVC module: {echo_string}")


@app.command()
def pull():
    """
    Retrieves the images from the DVC remote storage.
    """
    typer.echo("Importing images from DVC storage")


if __name__ == "__main__":
    app()
