from dataclasses import dataclass

from modules.authority.domain.model.session import Session
from modules.authority.domain.model.tenant import Tenant
from modules.authority.domain.model.user import User


@dataclass(init=True, unsafe_hash=True, frozen=True)
class TenantDpo:
    tenant: Tenant


@dataclass(init=True, unsafe_hash=True, frozen=True)
class SessionDpo:
    session: Session


@dataclass(init=True, unsafe_hash=True, frozen=True)
class UserDpo:
    user: User
    tenants: list[Tenant]

    def has_tenant(self, tenant_id: str) -> bool:
        for e in self.tenants:
            if e.id.value == tenant_id:
                return True
        return False
