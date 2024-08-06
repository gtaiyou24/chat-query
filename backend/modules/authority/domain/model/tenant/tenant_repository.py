from __future__ import annotations

import abc

from modules.authority.domain.model.tenant import TenantId, Tenant


class TenantRepository(abc.ABC):
    @abc.abstractmethod
    def next_identity(self) -> TenantId:
        pass

    @abc.abstractmethod
    def add(self, tenant: Tenant) -> None:
        pass

    @abc.abstractmethod
    def remove(self, tenant: Tenant) -> None:
        pass

    @abc.abstractmethod
    def get(self, tenant_id: TenantId) -> Tenant | None:
        pass
