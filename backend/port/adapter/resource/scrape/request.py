from __future__ import annotations

from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator


class ScrapeRequest(BaseModel):
    url: str | None = Field(
        default=None,
        title="URL",
        description="スクレイピング先の URL です。URL が指定されたら該当 URL から HTML を取得し、スクレイピングします。"
    )
    html: str | None = Field(default=None, title="HTML", description="スクレイピングする HTML を指定してください。")
    json_schema: dict = Field(title="JSON Schema", description="スクレイピングするデータの形式を Json Schema で指定してください。")

    @field_validator('json_schema', mode='before')
    def validate_json_schema(cls, v):
        if v == {}:
            raise ValueError('JSON Schema が空です。{"type": "object", "properties": {...}} の形式で指定してください。')
        return v

    @field_validator('html', mode='before')
    def validate_html(cls, v):
        if v is not None and v == '':
            raise ValueError('HTML に空文字が指定されました。指定する場合は、html タグを指定してください。')
        return v

    @model_validator(mode="after")
    def validate_url_and_html(self) -> Self:
        """URL または HTML のいずれかが指定されていること"""
        if self.url is self.html is None:
            raise ValueError("URL と HTML が未指定です。URL もしくは HTML を指定してください。")
        return self
