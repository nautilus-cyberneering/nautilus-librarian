from nautilus_librarian.mods.dvc.domain.diff.renamed_path import RenamedPath


def it_should_contain_the_old_and_new_relative_paths_for_a_renamed_file():

    assert (
        str(RenamedPath("data/000001/32/000001-32.600.2.tif", "data/000002/32/000002-32.600.2.tif"))
        == "data/000001/32/000001-32.600.2.tif"
    )
