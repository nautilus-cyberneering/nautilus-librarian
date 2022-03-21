from nautilus_librarian.mods.dvc.domain.diff.parser import Parser


def extract_all_added_and_renamed_files_from_dvc_diff(dvc_diff_json):
    dvc_diff = Parser.from_json(dvc_diff_json)
    all_files = dvc_diff.filter(exclude_deleted=True, exclude_modified=True)
    return all_files


def extract_added_files_from_dvc_diff(dvc_diff_json):
    dvc_diff = Parser.from_json(dvc_diff_json)
    return dvc_diff.filter(
        exclude_deleted=True, exclude_modified=True, exclude_renamed=True
    ).as_plain_list()
