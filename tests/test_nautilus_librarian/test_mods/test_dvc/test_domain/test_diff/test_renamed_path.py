from nautilus_librarian.mods.dvc.domain.diff.renamed_path import RenamedPath


def it_should_contain_the_old_and_new_relative_paths_for_a_renamed_file():

    renamed_path = RenamedPath("data/new-file.txt", "data/old-file.txt")

    assert str(renamed_path) == "data/old-file.txt -> data/new-file.txt"
    assert str(renamed_path.new()) == "data/new-file.txt"
    assert str(renamed_path.old()) == "data/old-file.txt"
