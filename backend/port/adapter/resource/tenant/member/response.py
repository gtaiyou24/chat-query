from pydantic import BaseModel, Field


class MemberJson(BaseModel):
    pass


class MemberListJson(BaseModel):
    members: list[MemberJson] = Field(title="メンバー一覧")
