from enum import Enum


class ResultCode(Enum):
    CONTINUE = 0
    EXIT = 1
    ABORT = 2


class Message:
    NONE_MESSAGE = "__none_message__"

    def __init__(self, message: str):
        self.text = message

    def is_error(self):
        return False

    def is_empty_message(self):
        return self.text == Message.NONE_MESSAGE

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def __eq__(self, other_message) -> bool:
        return self.text == other_message.text

    @staticmethod
    def none():
        return Message(Message.NONE_MESSAGE)


class ErrorMessage(Message):
    def is_error(self):
        return True


class ActionResult:
    def __init__(self, code: ResultCode, messages: list[Message]):
        self.code = code
        self.messages = messages

    def contains_text(self, text: str):
        for message in self.messages:
            if text in message.text:
                return True
        return False

    def last_message(self) -> Message:
        if len(self.messages) == 0:
            return Message.none()
        return self.messages[-1]

    def last_message_text(self) -> str:
        if len(self.messages) == 0:
            return ""
        return self.messages[-1].text
