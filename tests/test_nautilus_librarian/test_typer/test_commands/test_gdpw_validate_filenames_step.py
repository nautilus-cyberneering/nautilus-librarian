import json

from typer.testing import CliRunner

from nautilus_librarian.main import app

runner = CliRunner()


def given_a_dvc_diff_object_it_should_validate_the_filename_of_the_new_media_files():

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = runner.invoke(
        app, ["gold-drawings-processing", json.dumps(dvc_diff, separators=(",", ":"))]
    )

    assert result.exit_code == 0
    assert "000001-32.600.2.tif ✓" in result.stdout


def given_a_dvc_diff_object_it_should_validate_the_filename_of_the_modified_media_files():

    dvc_diff = {
        "added": [],
        "deleted": [],
        "modified": [
            {"path": "data/000002/32/000002-32.600.2.tif"},
        ],
        "renamed": [],
    }

    result = runner.invoke(
        app, ["gold-drawings-processing", json.dumps(dvc_diff, separators=(",", ":"))]
    )

    assert result.exit_code == 0
    assert "000002-32.600.2.tif ✓" in result.stdout


def given_a_dvc_diff_object_it_should_validate_the_filename_of_the_renamed_media_files():

    dvc_diff = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [
            {"path": "data/000003/32/000003-32.600.2.tif"},
        ],
    }

    result = runner.invoke(
        app, ["gold-drawings-processing", json.dumps(dvc_diff, separators=(",", ":"))]
    )

    assert result.exit_code == 0
    assert "000003-32.600.2.tif ✓" in result.stdout


def given_a_wrong_media_filename_it_should_show_an_error_and_abort_the_command():

    dvc_diff_with_wrong_filename = {
        "added": [
            {"path": "data/000001/32/000001-9999999.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = runner.invoke(
        app,
        [
            "gold-drawings-processing",
            json.dumps(dvc_diff_with_wrong_filename, separators=(",", ":")),
        ],
    )

    assert result.exit_code == 1
    assert (
        "000001-9999999.600.2.tif ✗ Wrong purpose code. Purpose code should be: 32 or 42\nAborted!\n"
        in result.stdout
    )
