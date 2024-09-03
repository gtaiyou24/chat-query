from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Message:
    class Role(Enum):
        USER = 'user'
        SYSTEM = 'system'
        ASSISTANT = 'assistant'

        def __call__(self, content: str) -> Message:
            return Message(self, content)

    role: Role
    content: str

    @property
    def payload(self) -> dict:
        return {'role': self.role.value, 'content': self.content}
