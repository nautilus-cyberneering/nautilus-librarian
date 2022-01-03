from pathlib import Path

from nautilus_librarian.mods.console.domain.utils import (
    execute_console_command,
    execute_shell_command,
    shell_escape_arguments,
)


def test_execute_console_command():
    output = execute_console_command("echo hello")

    assert "hello" in output


def test_ignore_empty_commands():
    output = execute_console_command("")
    assert "" in output

    output = execute_console_command(
        """
    """
    )
    assert "" in output


def test_strip_white_spaces(temp_dir):
    output = execute_console_command("  pwd", cwd=temp_dir)

    assert Path(output.strip()) == temp_dir


def test_execute_multi_line_command():
    output = execute_console_command(
        """
        echo hello
        echo world
    """
    )

    assert "hello\nworld" in output


def test_execute_console_command_changing_the_current_working_dir(temp_dir):
    output = execute_console_command("pwd", cwd=temp_dir)

    assert str(temp_dir) in output


def test_execute_console_command_passing_variables(temp_dir):
    output = execute_console_command("echo {message}", message="hello world")

    assert "hello world" in output


def test_shell_escape_arguments():
    keyword_arguments = {"arg": "value"}

    escaped_kwargs = shell_escape_arguments(**keyword_arguments)

    assert escaped_kwargs == {"arg": "value"}

    keyword_arguments = {"arg": "value1 value 2"}

    escaped_kwargs = shell_escape_arguments(**keyword_arguments)

    assert escaped_kwargs == {"arg": "'value1 value 2'"}


def test_execute_shell_command(temp_dir):
    # Assert shell is being called using env vars
    output = execute_shell_command('MESSAGE="hello world"; echo $MESSAGE')
    assert output == "hello world\n"

    # Assert cwd argument is passed correctly
    output = execute_shell_command("pwd", cwd=temp_dir)
    assert Path(output.strip()) == temp_dir

    # Assert vars are passed correctly
    output = execute_shell_command("echo {message}", message="hello world")
    assert output == "hello world\n"
