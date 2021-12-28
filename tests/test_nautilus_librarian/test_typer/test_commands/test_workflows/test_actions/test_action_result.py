from nautilus_librarian.typer.commands.workflows.actions.action_result import (
    ActionResult,
    ErrorMessage,
    Message,
    ResultCode,
)


def it_should_store_messages():
    action_result = ActionResult(ResultCode.CONTINUE, [Message("hello world")])
    assert action_result.contains_text("hello world")


def it_should_store_error_messages():
    action_result = ActionResult(
        ResultCode.CONTINUE, [ErrorMessage("world is collapsing")]
    )
    assert action_result.contains_text("world is collapsing")


def it_should_return_the_last_message():
    action_result = ActionResult(ResultCode.CONTINUE, [ErrorMessage("world is nice")])
    assert action_result.last_message() == Message("world is nice")
