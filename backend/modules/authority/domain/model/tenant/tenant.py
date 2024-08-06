from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from modules.authority.domain.model.tenant import TenantId


@dataclass(init=True, eq=False)
class Tenant:
    class Type(Enum):
        PERSONAL = 'personal'
        ORGANIZATION = 'organization'

        def is_personal(self) -> bool:
            return self == Tenant.Type.PERSONAL

        def is_organization(self) -> bool:
            return self == Tenant.Type.ORGANIZATION

    id: TenantId
    name: str
    type: Type

    def __hash__(self):
        return hash(self.id.value)

    def __eq__(self, other: Tenant):
        if not isinstance(other, Tenant):
            return False
        return self.id == other.id
