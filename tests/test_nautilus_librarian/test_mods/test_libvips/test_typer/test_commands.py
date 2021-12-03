from nautilus_librarian.main import app
from typer.testing import CliRunner

runner = CliRunner()


def test_libvips_test_command():
    result = runner.invoke(app, ["libvips", "test", "hello"])
    assert result.exit_code == 0
    assert "Testing LibVips module: hello" in result.stdout
