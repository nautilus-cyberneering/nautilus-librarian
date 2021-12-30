import os

from test_nautilus_librarian.test_typer.test_commands.test_workflows.test_gold_images_processing import (
    copy_media_file_to_its_folder,
    create_initial_state,
)
from test_nautilus_librarian.utils import compact_json

from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.typer.commands.workflows.actions.dvc_pull_action import (
    dvc_pull_action,
)


def given_a_dvc_diff_object_with_a_new_gold_image_it_should_pull_the_image_from_the_remote_dvc_storage(
    temp_git_dir,
    temp_dvc_local_remote_storage_dir,
    temp_gpg_home_dir,
    git_user,
    sample_gold_image_absolute_path,
    sample_base_image_absolute_path,
):
    remote_name = "localremote"

    create_initial_state(
        temp_git_dir,
        temp_dvc_local_remote_storage_dir,
        sample_base_image_absolute_path,
        temp_gpg_home_dir,
        git_user,
        remote_name,
    )

    copy_media_file_to_its_folder(sample_gold_image_absolute_path, temp_git_dir)

    # Add the new Gold image and remove the local copy of the image
    execute_console_command(
        f"""
        dvc add data/000001/32/000001-32.600.2.tif
        dvc push
        git add data/000001/32/000001-32.600.2.tif.dvc data/000001/32/.gitignore
        GNUPGHOME={temp_gpg_home_dir} git commit -S --gpg-sign={git_user.signingkey} -m "feat: new gold image: 000001-32.600.2.tif" --author="{git_user.name} <{git_user.email}>" # noqa
        rm data/000001/32/000001-32.600.2.tif
    """,
        cwd=temp_git_dir,
    )

    dvcApiWrapper = DvcApiWrapper(temp_git_dir)
    dvc_diff_dict = dvcApiWrapper.diff("HEAD^", "HEAD")

    # Assert Gold image does not exist
    assert not os.path.exists(f"{temp_git_dir}/data/000001/32/000001-32.600.2.tif")

    # We pull the Gold image from the local remote storage
    dvc_pull_action(compact_json(dvc_diff_dict), str(temp_git_dir), remote_name)

    # Assert Gold image was pulled from the local remote storage
    assert os.path.isfile(f"{temp_git_dir}/data/000001/32/000001-32.600.2.tif")
