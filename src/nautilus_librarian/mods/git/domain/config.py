from nautilus_librarian.mods.console.domain.utils import execute_console_command
from nautilus_librarian.mods.git.domain.git_user import GitUser


def git_config_global_user():
    """
    It return the git global user configuration.

    It parses the config values from the git console command.

    TODO:
        * Check if we can use https://gitpython.readthedocs.io/en/stable/index.html.
        * We could write a wrapper: GitConfig(git_repo_dir). Like GitRepo class.
    """
    name = execute_console_command("git config --global --get user.name").strip()

    email = execute_console_command("git config --global --get user.email").strip()

    signingkey = execute_console_command(
        "git config --global --get user.signingkey"
    ).strip()

    return GitUser(name, email, signingkey)


def default_git_user_name():
    git_config_global_user().name


def default_git_user_email():
    git_config_global_user().email


def default_git_user_signingkey():
    git_config_global_user().signingkey
