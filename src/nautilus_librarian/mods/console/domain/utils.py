import os
import subprocess  # nosec


def get_current_working_directory():
    return os.getcwd()


def change_current_working_directory(new_dir):
    return os.chdir(new_dir)


def debug_execute_console_command(multiline_command: str, cwd=None) -> str:
    return execute_console_command(
        multiline_command, print_output=True, print_command=True, cwd=cwd
    )


def execute_console_command(
    multiline_command, print_output=False, print_command=False, cwd=None
) -> str:

    commands = multiline_command.splitlines()

    full_output = ""

    for command in commands:

        if print_command:
            print(command.strip())

        # TODO: Security Review
        process = subprocess.run(
            command,
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
