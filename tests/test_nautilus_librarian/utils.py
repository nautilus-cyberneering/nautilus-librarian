import pathlib
import subprocess  # nosec


def debug_execute_console_command(multiline_command):
    return execute_console_command(
        multiline_command, print_output=True, print_command=True
    )


def execute_console_command(multiline_command, print_output=False, print_command=False):

    commands = multiline_command.splitlines()

    full_output = ""

    for command in commands:

        if print_command:
            print(command.strip())

        process = subprocess.run(
            command,
            shell=True,  # nosec
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )

        output = process.stdout

        if print_output:
            print(output)

        full_output += output

    return full_output


def get_fixtures_dir():
    return pathlib.Path().resolve() / "tests/fixtures"
