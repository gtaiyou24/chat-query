from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    class Message(BaseModel):
        role: Literal['user', 'system', 'assistant'] = Field(title="ロール", default='user')
        content: str = Field(title="コンテンツ")

    messages: list[Message] = Field(title="メッセージ一覧")
