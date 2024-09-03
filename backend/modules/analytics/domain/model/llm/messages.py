from __future__ import annotations

from dataclasses import dataclass

from modules.analytics.domain.model.llm import Message


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Messages:
    list: list[Message]

    @staticmethod
    def thread(*message: Message) -> Messages:
        return Messages(list(message))

    def replay(self, message: Message) -> Messages:
        _list = [e for e in self.list]
        _list.append(message)
        return Messages(_list)
