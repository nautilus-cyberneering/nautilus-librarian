import json

from test_nautilus_librarian.test_typer.test_commands.test_gold_drawings_processing_workflow import (
    create_initial_state,
)
from test_nautilus_librarian.utils import compact_json
from typer.testing import CliRunner

from nautilus_librarian.main import app

runner = CliRunner()


def given_a_dvc_diff_object_it_should_validate_the_filename_of_the_new_media_files(
    temp_git_dir, temp_dvc_local_remote_storage_dir, sample_base_image_absolute_path
):
    create_initial_state(
        temp_git_dir, temp_dvc_local_remote_storage_dir, sample_base_image_absolute_path
    )

    dvc_diff_with_added_gold_image = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    # Execute the workflow
    result = runner.invoke(
        app,
        ["gold-drawings-processing", compact_json(dvc_diff_with_added_gold_image)],
        env={"INPUT_GIT_REPO_DIR": str(temp_git_dir)},
    )

    assert result.exit_code == 0
    assert "000001-32.600.2.tif ✓" in result.stdout


def given_a_dvc_diff_object_it_should_validate_the_filename_of_the_modified_media_files(
    temp_git_dir,
):
    dvc_diff_with_modified_image = {
        "added": [],
        "deleted": [],
        "modified": [
            {"path": "data/000002/32/000002-32.600.2.tif"},
        ],
        "renamed": [],
    }

    # Execute the workflow
    result = runner.invoke(
        app,
        [
            "gold-drawings-processing",
            json.dumps(dvc_diff_with_modified_image, separators=(",", ":")),
        ],
        env={"INPUT_GIT_REPO_DIR": str(temp_git_dir)},
    )

    assert result.exit_code == 0
    assert "000002-32.600.2.tif ✓" in result.stdout


def given_a_dvc_diff_object_it_should_validate_the_filename_of_the_renamed_media_files(
    temp_git_dir,
):
    dvc_diff_with_renamed_image = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [
            {"path": "data/000003/32/000003-32.600.2.tif"},
        ],
    }

    # Execute the workflow
    result = runner.invoke(
        app,
        ["gold-drawings-processing", compact_json(dvc_diff_with_renamed_image)],
        env={"INPUT_GIT_REPO_DIR": str(temp_git_dir)},
    )

    assert result.exit_code == 0
    assert "000003-32.600.2.tif ✓" in result.stdout


def given_a_wrong_media_filename_it_should_show_an_error_and_abort_the_command(
    temp_git_dir,
):
    dvc_diff_with_wrong_filename = {
        "added": [
            {"path": "data/000001/32/000001-9999999.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    # Execute the workflow
    result = runner.invoke(
        app,
        ["gold-drawings-processing", compact_json(dvc_diff_with_wrong_filename)],
        env={"INPUT_GIT_REPO_DIR": str(temp_git_dir)},
    )

    assert result.exit_code == 1
    assert (
        "000001-9999999.600.2.tif ✗ Wrong purpose code. Purpose code should be: 32 or 42\nAborted!\n"
        in result.stdout
    )
