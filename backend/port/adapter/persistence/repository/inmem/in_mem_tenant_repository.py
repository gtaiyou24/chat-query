from __future__ import annotations

import uuid
from typing import override

from modules.authority.domain.model.tenant import TenantRepository, Tenant, TenantId
from modules.authority.domain.model.user import UserId


class InMemTenantRepository(TenantRepository):
    values: set[Tenant] = set()

    @override
    def next_identity(self) -> TenantId:
        return TenantId(str(uuid.uuid4()))

    def add(self, tenant: Tenant) -> None:
        self.values.add(tenant)

    def remove(self, tenant: Tenant) -> None:
        self.values.remove(tenant)

    def get(self, tenant_id: TenantId) -> Tenant | None:
        for e in self.values:
            if e.id == tenant_id:
                return e
        return None

    def tenants_with_user_id(self, user_id: UserId) -> set[Tenant]:
        tenants = set()
        for e in self.values:
            for m in e.members:
                if m.user_id == user_id:
                    tenants.add(e)
                    break
        return tenants
