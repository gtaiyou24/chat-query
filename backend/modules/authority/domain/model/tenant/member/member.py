from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from modules.authority.domain.model.tenant import TenantId
from modules.authority.domain.model.tenant.member import MemberId
from modules.authority.domain.model.user import UserId


@dataclass(init=True, eq=False)
class Member:
    class Role(Enum):
        OWNER = 'オーナー'
        EDITOR = '編集者'
        READER = '閲覧者'

    id: MemberId
    tenant_id: TenantId
    user_id: UserId
    role: Role

    def __eq__(self, other: Member):
        if not isinstance(other, Member):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id.value)
