import os
from typing import List

from nautilus_librarian.domain.file_locator import (
    file_locator,
    guard_that_base_image_exists,
)
from nautilus_librarian.mods.dvc.domain.dvc_services_api import DvcServicesApi
from nautilus_librarian.mods.dvc.domain.utils import (
    extract_added_files_from_dvc_diff,
    extract_deleted_files_from_dvc_diff,
    extract_modified_files_from_dvc_diff,
    extract_renamed_files_from_dvc_diff,
)
from nautilus_librarian.mods.git.domain.git_user import GitUser
from nautilus_librarian.mods.git.domain.repo import GitRepo
from nautilus_librarian.mods.namecodes.domain.filename import Filename
from nautilus_librarian.mods.namecodes.domain.filename_filters import filter_gold_images
from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    Message,
    ResultCode,
)


def format_extracted_files(files):
    """
    Parses a list of images from dvc diff output in json format, filters the Gold
    images and returns a list of Filenames.
    """
    gold_images = filter_gold_images(files)
    return [Filename(gold_image) for gold_image in gold_images]


def get_new_gold_images_filenames_from_dvc_diff(dvc_diff) -> List[Filename]:
    return format_extracted_files(extract_added_files_from_dvc_diff(dvc_diff))


def get_modified_gold_images_filenames_from_dvc_diff(dvc_diff) -> List[Filename]:
    return format_extracted_files(extract_modified_files_from_dvc_diff(dvc_diff))


def get_deleted_gold_images_filenames_from_dvc_diff(dvc_diff) -> List[Filename]:
    return format_extracted_files(extract_deleted_files_from_dvc_diff(dvc_diff))


def get_renamed_gold_images_filenames_from_dvc_diff(
    dvc_diff,
) -> List[tuple[Filename, Filename]]:
    extracted_filenames = extract_renamed_files_from_dvc_diff(dvc_diff)
    old_filenames = [element["old"] for element in extracted_filenames]
    new_filenames = [element["new"] for element in extracted_filenames]
    return list(
        zip(
            format_extracted_files(old_filenames), format_extracted_files(new_filenames)
        )
    )


def commit_new_and_modified_base_image(
    git_repo_dir, base_img_relative_path, gnupghome, git_user, is_new=True
):

    repo = GitRepo(git_repo_dir, git_user, gnupghome)
    dvc_services = DvcServicesApi(git_repo_dir)

    files_to_commit = dvc_services.get_files_to_commit(base_img_relative_path)
    verb = "new" if is_new else "modified"

    return repo.commit(
        {"added": files_to_commit},
        commit_message=f"feat: {verb} base image: {os.path.basename(base_img_relative_path)}",
    )


def commit_deleted_base_image(
    git_repo_dir, base_img_relative_path, gnupghome, git_user
):
    repo = GitRepo(git_repo_dir, git_user, gnupghome)
    dvc_services = DvcServicesApi(git_repo_dir)

    return repo.commit(
        {"deleted": dvc_services.get_files_to_commit(base_img_relative_path)},
        commit_message=f"feat: deleted base image: {os.path.basename(base_img_relative_path)}",
    )


def commit_renamed_base_image(
    git_repo_dir,
    old_base_img_relative_path,
    new_base_img_relative_path,
    gnupghome,
    git_user,
):
    repo = GitRepo(git_repo_dir, git_user, gnupghome)
    dvc_services = DvcServicesApi(git_repo_dir)

    return repo.commit(
        {
            "renamed": {
                "old": dvc_services.get_files_to_commit(old_base_img_relative_path),
                "new": dvc_services.get_files_to_commit(new_base_img_relative_path),
            }
        },
        commit_message=(
            f"feat: renamed base image: {os.path.basename(old_base_img_relative_path)}"
            f" -> {os.path.basename(new_base_img_relative_path)}"
        ),
    )


def calculate_the_corresponding_base_image_from_gold_image(git_repo_dir, gold_image):
    """
    Returns the Base image path which correspond to the given Gold image.

    Code Review: LibraryFilePath class? and rename Filename to LibraryFilename?
    """
    corresponding_base_image = gold_image.generate_base_image_filename()
    corresponding_base_image_relative_path = (
        file_locator(corresponding_base_image) + "/" + str(corresponding_base_image)
    )
    corresponding_base_image_absolute_path = (
        git_repo_dir + "/" + corresponding_base_image_relative_path
    )
    return (
        corresponding_base_image_relative_path,
        corresponding_base_image_absolute_path,
    )


def process_added_base_images(
    gold_images_list, messages, git_repo_dir, gnupghome, git_user
):

    for gold_image in gold_images_list:
        (
            base_img_relative_path,
            base_img_absolute_path,
        ) = calculate_the_corresponding_base_image_from_gold_image(
            git_repo_dir, gold_image
        )

        guard_that_base_image_exists(base_img_absolute_path)

        commit_new_and_modified_base_image(
            git_repo_dir, base_img_relative_path, gnupghome, git_user
        )

        messages.append(
            Message(
                f"New Gold image found: {gold_image} -> Base image: {base_img_relative_path} ✓"
            )
        )


def process_deleted_base_images(
    gold_images_list, messages, git_repo_dir, gnupghome, git_user
):

    for gold_image in gold_images_list:
        (
            base_img_relative_path,
            _,
        ) = calculate_the_corresponding_base_image_from_gold_image(
            git_repo_dir, gold_image
        )

        commit_deleted_base_image(
            git_repo_dir, base_img_relative_path, gnupghome, git_user
        )

        messages.append(
            Message(
                f"New Gold image deleted: {gold_image} -> Base image: {base_img_relative_path} ✓"
            )
        )


def process_modified_base_images(
    gold_images_list,
    messages,
    git_repo_dir,
    gnupghome,
    git_user,
):
    for gold_image in gold_images_list:
        (
            base_img_relative_path,
            base_img_absolute_path,
        ) = calculate_the_corresponding_base_image_from_gold_image(
            git_repo_dir, gold_image
        )
        guard_that_base_image_exists(base_img_absolute_path)

        commit_new_and_modified_base_image(
            git_repo_dir, base_img_relative_path, gnupghome, git_user, is_new=False
        )

        messages.append(
            Message(
                f"Modified Gold image found: {gold_image} -> Base image: {base_img_relative_path} ✓"
            )
        )


def process_renamed_base_images(
    old_and_new_gold_images_list, messages, git_repo_dir, gnupghome, git_user
):
    # See note at https://dvc.org/doc/command-reference/diff#example-renamed-files
    # dvc diff only detects files which have been renamed but are otherwise unmodified.
    # Also, remember to commit new and OLD pointers
    for gold_image_duple in old_and_new_gold_images_list:
        old_gold_image = gold_image_duple[0]
        new_gold_image = gold_image_duple[1]
        (
            old_base_img_relative_path,
            _,
        ) = calculate_the_corresponding_base_image_from_gold_image(
            git_repo_dir, old_gold_image
        )
        (
            new_base_img_relative_path,
            _,
        ) = calculate_the_corresponding_base_image_from_gold_image(
            git_repo_dir, new_gold_image
        )

        commit_renamed_base_image(
            git_repo_dir,
            old_base_img_relative_path,
            new_base_img_relative_path,
            gnupghome,
            git_user,
        )

        messages.append(
            Message(
                f"New Gold image renamed: {old_gold_image} -> {new_gold_image} "
                f"Base image: {new_base_img_relative_path} -> {old_base_img_relative_path} ✓"
            )
        )

    return


def auto_commit_base_images(dvc_diff, git_repo_dir, gnupghome, git_user: GitUser):
    """
    Workflow step: auto-commit new Base images generated during the workflow execution
    in previous steps.

    Case 1. Added Gold images.
    For each added Gold image:
      [✓] 1. Calculate the corresponding Base image filename and filepath.
      [✓] 2. Check if the Base image exists.
      [✓] 3. Add the image to dvc.
      [✓] 4. Push the image to remote dvc storage.
      [✓] 5. Commit the image to the current branch with a signed commit.

    Points 2 to 5 are different depending on whether we are adding,
    modifying or renaming the Gold image.

    TODO:
    Case 2. Modified Gold images.
    For each modified Gold image:
      [ ] 1. ??
      [ ] 2. ...
      [ ] 3. ??
    Pending to define:
    https://github.com/Nautilus-Cyberneering/chinese-ideographs/pull/122#issuecomment-972844365

    Case 3. Renamed Gold images.
    For each renamed Gold image:
      [ ] 1. ??
      [ ] 2. ...
      [ ] 3. ??
    Pending to define:
    https://github.com/Nautilus-Cyberneering/chinese-ideographs/pull/122#issuecomment-972844365
    """

    messages: List[str] = []

    new_gold_images = get_new_gold_images_filenames_from_dvc_diff(dvc_diff)
    process_added_base_images(
        new_gold_images, messages, git_repo_dir, gnupghome, git_user
    )

    modified_gold_images = get_modified_gold_images_filenames_from_dvc_diff(dvc_diff)
    process_modified_base_images(
        modified_gold_images, messages, git_repo_dir, gnupghome, git_user
    )

    renamed_gold_images = get_renamed_gold_images_filenames_from_dvc_diff(dvc_diff)
    process_renamed_base_images(
        renamed_gold_images, messages, git_repo_dir, gnupghome, git_user
    )

    deleted_gold_images = get_deleted_gold_images_filenames_from_dvc_diff(dvc_diff)
    process_deleted_base_images(
        deleted_gold_images, messages, git_repo_dir, gnupghome, git_user
    )

    return ActionResult(ResultCode.CONTINUE, messages)
