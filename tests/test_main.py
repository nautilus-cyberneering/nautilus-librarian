from typer.testing import CliRunner

from nautilus_librarian.main import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Testing main module: hello" in result.stdout
