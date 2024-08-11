from enum import Enum

from pydantic import BaseModel, Field


class Role(str, Enum):
    ADMIN = 'admin'
    EDITOR = 'editor'
    READER = 'reader'


class InviteMemberRequest(BaseModel):
    email_address: str = Field(title="メールアドレス")
    role: Role = Field(title="ロール")


class ChangeRoleRequest(BaseModel):
    member_id: str = Field(title="メンバーID")
    new_role: Role = Field(title="新しいロール")
