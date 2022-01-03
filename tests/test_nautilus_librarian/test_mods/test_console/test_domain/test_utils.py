from nautilus_librarian.mods.console.domain.utils import (
    execute_console_command,
    shell_escape_arguments,
)


def test_execute_console_command():
    output = execute_console_command("echo hello")

    assert "hello" in output


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
