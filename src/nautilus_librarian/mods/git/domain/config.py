from nautilus_librarian.mods.git.domain.git_command_wrapper import git
from nautilus_librarian.mods.git.domain.git_user import GitUser


def git_config_global_user() -> GitUser:
    """
    It returns the git global user configuration.
    """
    return git().get_global_user()


def default_git_user_name() -> str:
    return git_config_global_user().name


def default_git_user_email() -> str:
    return git_config_global_user().email


def default_git_user_signingkey() -> str:
    return git_config_global_user().signingkey
