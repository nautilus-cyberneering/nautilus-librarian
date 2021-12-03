import typer

app = typer.Typer()


@app.command()
def test(echo_string: str):
    """
    It's only used for testing purposes
    """
    typer.echo(f"Testing GPG module: {echo_string}")


if __name__ == "__main__":
    app()
