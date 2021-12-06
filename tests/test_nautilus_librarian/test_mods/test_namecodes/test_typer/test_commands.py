from typer.testing import CliRunner

from nautilus_librarian.main import app

runner = CliRunner()


def test_namecodes_test_command():
    result = runner.invoke(app, ["namecodes", "test", "hello"])
    assert result.exit_code == 0
    assert "Testing Namecode module: hello" in result.stdout
