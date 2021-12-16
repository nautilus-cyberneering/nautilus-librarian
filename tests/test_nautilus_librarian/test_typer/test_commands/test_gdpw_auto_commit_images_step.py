import json

from test_nautilus_librarian.test_typer.test_commands.test_gold_drawings_processing_workflow import (
    create_initial_state,
)
from test_nautilus_librarian.utils import execute_console_command
from typer.testing import CliRunner

from nautilus_librarian.main import app
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.typer.commands.gold_drawings_processing_workflow import (
    extract_new_gold_images_from_dvc_diff,
)

runner = CliRunner()


def given_a_dvc_diff_object_with_a_new_gold_image_it_should_commit_the_added_base_image_to_dvc(
    temp_git_dir, temp_dvc_local_remote_storage_dir, sample_base_image_absolute_path
):

    create_initial_state(
        temp_git_dir, temp_dvc_local_remote_storage_dir, sample_base_image_absolute_path
    )

    dvc_diff = {
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
        ["gold-drawings-processing", json.dumps(dvc_diff, separators=(",", ":"))],
        env={"INPUT_GIT_REPO_DIR": str(temp_git_dir)},
    )

    git_status_output = execute_console_command("git status")

    assert result.exit_code == 0
    assert "On branch" in git_status_output
    assert "000001-32.600.2.tif ✓\n" in result.stdout


def test_get_new_gold_images_from_dvc_diff():

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = extract_new_gold_images_from_dvc_diff(
        json.dumps(dvc_diff, separators=(",", ":"))
    )

    assert result == [Filename("data/000001/32/000001-32.600.2.tif")]
