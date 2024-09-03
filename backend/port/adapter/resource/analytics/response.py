from __future__ import annotations

from typing import Literal, Any

from pydantic import BaseModel, Field

from modules.analytics.application.dpo import DataSetDpo


class ChatResponse(BaseModel):
    class Message(BaseModel):
        role: Literal['user', 'system', 'assistant'] = Field(title="ロール")
        content: str = Field(title="コンテンツ")

    messages: list[Message] = Field(title="メッセージ一覧")


class DataSetResponse(BaseModel):
    class DataField(BaseModel):
        name: str = Field(title="フィールド名")

    fields: list[DataField] = Field(title="フィールド一覧")
    data_source: list[dict[str, Any]] = Field(title="データソース")
    query: str = Field(title="クエリー")

    @staticmethod
    def from_(dpo: DataSetDpo) -> DataSetResponse:
        return DataSetResponse(
            fields=[DataSetResponse.DataField(name=f.name) for f in dpo.dataset.fields],
            data_source=[row for row in dpo.dataset.data_source],
            query=dpo.query
        )
