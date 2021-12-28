from glob import glob

from namespace_modules_patch import apply_patch

apply_patch()

# Plugins


def from_filename_to_module(filepath):
    """
    Generate the module name to "import" from the file path.

    For example:
    From: tests/test_nautilus_librarian/test_mods/test_dvc/fixtures/dvc_fixtures.py
    To: test_nautilus_librarian.test_mods.test_dvc.fixtures.dvc_fixtures
    """
    filepath = filepath.replace("/", ".").replace(".py", "")

    prefix = "tests."
    prefix_len = len(prefix)
    if filepath.startswith(prefix):
        filepath = filepath[prefix_len:]

    return filepath


def get_the_list_of_mod_fixtures_modules():
    """
    Autoload fixtures from mods. This function gets the list of modules to import.
    Each mod can have a fixtures module with the suffix "_fixtures.py" in the "fixtures" fir.
    Credits: https://medium.com/@nicolaikozel/modularizing-pytest-fixtures-fd40315c5a93
    """
    return [
        from_filename_to_module(fixture_file)
        for fixture_file in glob(
            "tests/test_nautilus_librarian/**/fixtures/*_fixtures.py", recursive=True
        )
    ]


# Load plugins
# https://docs.pytest.org/en/latest/how-to/plugins.html#requiring-loading-plugins-in-a-test-module-or-conftest-file
pytest_plugins = get_the_list_of_mod_fixtures_modules()
