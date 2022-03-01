import os
from shutil import copytree

from test_nautilus_librarian.test_typer.test_commands.test_workflows.test_gold_images_processing import (
    add_gold_image,
    create_initial_state,
)
from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.dvc.domain.dvc_command_wrapper import dvc
from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.generate_base_images_action import (
    generate_base_images,
)


def copy_fixtures_to_tmp_path(fixtures_dir, temp_path):
    copytree(fixtures_dir, temp_path)


def given_a_diff_structure_with_added_gold_image_it_should_generate_base_image(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    sample_base_image_absolute_path,
    temp_gpg_home_dir,
    git_user,
    sample_gold_image_absolute_path,
):

    dvc_diff_with_added_gold_image = {
        "added": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    create_initial_state(
        temp_git_dir,
        temp_dvc_local_remote_storage_dir,
        sample_base_image_absolute_path,
        temp_gpg_home_dir,
        git_user,
    )
    add_gold_image(
        temp_git_dir, sample_gold_image_absolute_path, temp_gpg_home_dir, git_user
    )

    result = generate_base_images(
        compact_json(dvc_diff_with_added_gold_image), temp_git_dir, 512
    )

    # Assert Base image was created
    assert os.path.isfile(f"{temp_git_dir}/data/000001/52/000001-52.600.2.tif")

    # DVC Asserts

    # Assert dvc files were created
    assert os.path.isfile(f"{temp_git_dir}/data/000001/52/000001-52.600.2.tif.dvc")
    assert os.path.isfile(f"{temp_git_dir}/data/000001/52/.gitignore")

    # Assert Base image was pushed to local "remote" storage
    dvc_status_output_json = dvc(temp_git_dir).status_remote("localremote")
    expected_status_new = {"data/000001/52/000001-52.600.2.tif": "new"}
    expected_status_empty = {}
    assert (
        expected_status_new == dvc_status_output_json
        or expected_status_empty == dvc_status_output_json
    )

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text(
        "✓ Base image of data/000001/32/000001-32.600.2.tif successfully generated"
    )


def given_a_diff_structure_with_modified_gold_image_it_should_generate_base_image(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    sample_base_image_absolute_path,
    temp_gpg_home_dir,
    git_user,
    sample_gold_image_absolute_path,
):

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [],
        "modified": [
            {"path": "data/000001/32/000001-32.600.2.tif"},
        ],
        "renamed": [],
    }

    create_initial_state(
        temp_git_dir,
        temp_dvc_local_remote_storage_dir,
        sample_base_image_absolute_path,
        temp_gpg_home_dir,
        git_user,
    )
    add_gold_image(
        temp_git_dir, sample_gold_image_absolute_path, temp_gpg_home_dir, git_user
    )

    result = generate_base_images(
        compact_json(dvc_diff_with_added_gold_image), f"{temp_git_dir}", 512
    )

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text(
        "✓ Base image of data/000001/32/000001-32.600.2.tif successfully generated"
    )


def given_a_diff_structure_with_renamed_gold_image_it_should_not_generate_base_images(
    sample_gold_image_absolute_path,
):

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed": [
            {
                "path": {
                    "old": sample_gold_image_absolute_path,
                    "new": sample_gold_image_absolute_path,
                }
            },
        ],
    }

    result = generate_base_images(compact_json(dvc_diff_with_added_gold_image), "", 512)

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text("No Gold image changes found")
