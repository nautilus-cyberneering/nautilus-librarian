from enum import Enum


class ResultCode(Enum):
    CONTINUE = 0
    EXIT = 1
    ABORT = 2


class Message:
    def __init__(self, message: str):
        self.text = message

    def is_error(self):
        return False

    def __str__(self):
        return self.text


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
