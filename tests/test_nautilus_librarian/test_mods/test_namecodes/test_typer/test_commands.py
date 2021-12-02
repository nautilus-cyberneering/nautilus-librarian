from nautilus_librarian.main import app
from typer.testing import CliRunner

runner = CliRunner()


def test_app():
    result = runner.invoke(app, ["namecodes", "test", "hello"])
    assert result.exit_code == 0
    assert "Testing Namecode module: hello" in result.stdout
