from nautilus_librarian.main import app
from typer.testing import CliRunner

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["namecodes"])
    assert result.exit_code == 0
    assert "Testing main module: namecodes" in result.stdout
