from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.typer.commands.workflows.actions.action_result import ResultCode
from nautilus_librarian.typer.commands.workflows.actions.generate_base_images_action import (
    generate_base_images,
)


def given_a_diff_structure_and_size_limits_it_should_validate_new_image_dimensions(
    sample_gold_image_absolute_path, tmp_path_factory
):

    dvc_diff_with_added_gold_image = {
        "added": [
            {"path": sample_gold_image_absolute_path},
        ],
        "deleted": [],
        "modified": [],
        "renamed": [],
    }

    temp_path = tmp_path_factory.mktemp("repo")

    result = generate_base_images(
        compact_json(dvc_diff_with_added_gold_image), f"{temp_path}", 512
    )

    assert result.code == ResultCode.CONTINUE
    assert result.contains_text(
        f"✓ Base image of {sample_gold_image_absolute_path} successfully generated"
    )
