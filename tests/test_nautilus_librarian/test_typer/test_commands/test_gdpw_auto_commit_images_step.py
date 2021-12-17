import json
import os

from test_nautilus_librarian.test_typer.test_commands.test_gold_drawings_processing_workflow import (
    create_initial_state,
)
from test_nautilus_librarian.utils import compact_json
from typer.testing import CliRunner

from nautilus_librarian.main import app
from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.typer.commands.gold_drawings_processing_workflow import (
    get_new_gold_images_filenames_from_dvc_diff,
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
        ["gold-drawings-processing", compact_json(dvc_diff)],
        env={"INPUT_GIT_REPO_DIR": str(temp_git_dir)},
    )

    # debug_execute_console_command("tree -a data", cwd=temp_git_dir)

    # Assert command runned successfully
    assert result.exit_code == 0

    # Assert Base image was created
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/000001-42.600.2.tif")

    # Assert dvc files were created
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/000001-42.600.2.tif.dvc")
    assert os.path.isfile(f"{temp_git_dir}/data/000001/42/.gitignore")

    # Assert Base image was pushed to local "remote" storage
    dvc_status_output = execute_console_command(
        "dvc status --show-json --cloud --remote=localremote", cwd=temp_git_dir
    )
    dvc_status_output_json = json.loads(dvc_status_output)
    expected_status_new = {"data/000001/42/000001-42.600.2.tif": "new"}
    expected_status_empty = {}
    assert (
        expected_status_new == dvc_status_output_json
        or expected_status_empty == dvc_status_output_json
    )

    # Assert Base commit was created
    git_log_output = execute_console_command("git log --oneline", cwd=temp_git_dir)
    commit_message = "feat: new base image: 000001-42.600.2.tif"
    assert commit_message in git_log_output

    # TODO:
    #  * Assert commit is signed
    #  * Assert file content is OK?
    #  * Assert commit content is OK?


def test_get_new_gold_images_from_dvc_diff():

    dvc_diff = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
            {"path": "data/000001/42/000001-42.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    result = get_new_gold_images_filenames_from_dvc_diff(compact_json(dvc_diff))

    assert result == [Filename("data/000001/32/000001-32.600.2.tif")]
