from nautilus_librarian.typer.commands.workflows.actions.action_result import Message


def test_messages_can_be_compared():
    msg1 = Message("message 1")
    msg2 = Message("message 1")
    msg3 = Message("message 3")

    assert msg1 == msg2
    assert msg1 != msg3
