from typer.testing import CliRunner

from nautilus_librarian.main import app

runner = CliRunner()


def it_should_show_a_message_if_there_is_not_any_change_in_gold_images():
    result = runner.invoke(app, ["gold-drawings-processing"])

    assert result.exit_code == 0
    assert "No Gold image changes found" in result.stdout
