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
    **kwargs
) -> str:

    commands = multiline_command.splitlines()

    full_output = ""

    escaped_kwargs = shell_escape_arguments(**kwargs)

    for command in commands:

        formatted_cmd = command.format(**escaped_kwargs)

        if print_command:
            print(formatted_cmd.strip())

        # TODO: Security Review
        process = subprocess.run(
            formatted_cmd,
            shell=True,  # nosec
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
