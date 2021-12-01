import typer

app = typer.Typer()


@app.command()
def test(echo_string: str):
    typer.echo(f"Testing Nautilus Namecodes module: {echo_string}")


if __name__ == "__main__":
    app()
