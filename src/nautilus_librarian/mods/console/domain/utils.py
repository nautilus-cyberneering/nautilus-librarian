import os
import shlex
import subprocess  # nosec


def get_current_working_directory():
    return os.getcwd()


def change_current_working_directory(new_dir):
    return os.chdir(new_dir)


def shell_escape_arguments(**kwargs):
    escaped_kwargs = {}
    for key, value in kwargs.items():
        escaped_kwargs[key] = shlex.quote(str(value))
    return escaped_kwargs


def execute_console_command(
    multiline_command,
    vars={},
    print_output=False,
    print_command=False,
    cwd=None,
    shell=False,
    **kwargs
) -> str:

    commands = multiline_command.splitlines()

    full_output = ""

    escaped_kwargs = shell_escape_arguments(**kwargs)

    for command in commands:

        stripped_command = command.strip()

        if stripped_command == "":
            continue

        formatted_cmd = stripped_command.format(**escaped_kwargs)

        if print_command:
            print(formatted_cmd)

        if shell:
            process = subprocess.run(
                formatted_cmd,
                shell=True,  # nosec
                check=True,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                cwd=cwd,
            )
        else:
            process = subprocess.run(
                shlex.split(formatted_cmd),
                shell=False,  # nosec
                check=True,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                cwd=cwd,
            )

        output = process.stdout

        if print_output:
            print(output)

        full_output += output

    return full_output


def execute_shell_command(
    multiline_command,
    vars={},
    print_output=False,
    print_command=False,
    cwd=None,
    **kwargs
):
    """
    Wrapper to execute shell scripts. It is not recommended to use shell scripts:
    https://semgrep.dev/docs/cheat-sheets/python-command-injection/#1b-shelltrue
    This wrapper allow us to easily find parts of the code where we are using shell.

    It's needed for example, when we want to define env vars like this:
    GNUPGHOME=/gnupghome git commit ...
    """
    return execute_console_command(
        multiline_command,
        vars=vars,
        print_output=print_output,
        print_command=print_command,
        cwd=cwd,
        shell=True,  # nosec
        **kwargs
    )
