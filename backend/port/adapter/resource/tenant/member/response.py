from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from modules.authority.application.member.dpo import MembersDpo, MemberDpo


class MemberJson(BaseModel):
    user_id: str = Field(title="ユーザーID")
    username: str = Field(title="ユーザー名")
    email_address: str = Field(title="メールアドレス")
    role: Literal['ADMIN', 'EDITOR', 'READER'] = Field(title="ロール")

    @staticmethod
    def from_(dpo: MemberDpo) -> MemberJson:
        return MemberJson(
            user_id=dpo.member.user_id.value,
            username=dpo.user.username,
            email_address=dpo.user.email_address.text,
            role=dpo.member.role.name
        )


class MemberListJson(BaseModel):
    members: list[MemberJson] = Field(title="メンバー一覧")

    @staticmethod
    def from_(dpo: MembersDpo) -> MemberListJson:
        return MemberListJson(members=[MemberJson.from_(member_dpo) for member_dpo in dpo.list_member_dpo])
