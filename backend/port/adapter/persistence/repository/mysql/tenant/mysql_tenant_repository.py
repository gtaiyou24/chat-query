from __future__ import annotations

import uuid
from typing import override

from modules.authority.domain.model.tenant import TenantRepository, Tenant, TenantId
from modules.authority.domain.model.user import UserId


class MySQLTenantRepository(TenantRepository):
    @override
    def next_identity(self) -> TenantId:
        return TenantId(str(uuid.uuid4()))

    @override
    def add(self, tenant: Tenant) -> None:
        pass

    @override
    def remove(self, tenant: Tenant) -> None:
        pass

    @override
    def get(self, tenant_id: TenantId) -> Tenant | None:
        pass

    @override
    def tenants_with_user_id(self, user_id: UserId) -> set[Tenant]:
        pass