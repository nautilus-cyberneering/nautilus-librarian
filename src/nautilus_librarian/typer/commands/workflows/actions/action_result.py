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

    def last_message(self) -> ErrorMessage:
        if len(self.messages) == 0:
            return None
        return self.messages[-1]

    def last_message_text(self) -> str:
        if len(self.messages) == 0:
            return ""
        return self.messages[-1].text
