from typer.testing import CliRunner

from nautilus_librarian.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Librarian Version: 0.0.0" in result.stdout
