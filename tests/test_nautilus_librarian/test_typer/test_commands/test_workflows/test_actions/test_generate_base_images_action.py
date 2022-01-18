from shutil import copytree

from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.generate_base_images_action import (
    generate_base_images,
)


def copy_fixtures_to_tmp_path(fixtures_dir, temp_path):
    copytree(fixtures_dir, temp_path)


def given_a_diff_structure_with_added_gold_image_it_should_generate_base_image(
    sample_gold_image_relative_path, tmp_path_factory, workflows_fixtures_dir
):

    dvc_diff_with_added_gold_image = {
        "added": [
            {"path": sample_gold_image_relative_path},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    temp_path = tmp_path_factory.mktemp("repo")
    copy_fixtures_to_tmp_path(
        f"{workflows_fixtures_dir}/images", f"{temp_path}/test_repo/images"
    )

    result = generate_base_images(
        compact_json(dvc_diff_with_added_gold_image), f"{temp_path}/test_repo", 512
    )

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text(
        f"✓ Base image of {sample_gold_image_relative_path} successfully generated"
    )


def given_a_diff_structure_with_modified_gold_image_it_should_generate_base_image(
    sample_gold_image_relative_path, tmp_path_factory, workflows_fixtures_dir
):

    dvc_diff_with_added_gold_image = {
        "added": [],
        "deleted": [],
        "modified": [
            {"path": sample_gold_image_relative_path},
        ],
        "renamed": [],
    }

    temp_path = tmp_path_factory.mktemp("repo")
    copy_fixtures_to_tmp_path(workflows_fixtures_dir, f"{temp_path}/test_repo")

    result = generate_base_images(
        compact_json(dvc_diff_with_added_gold_image), f"{temp_path}/test_repo", 512
    )

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text(
        f"✓ Base image of {sample_gold_image_relative_path} successfully generated"
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
