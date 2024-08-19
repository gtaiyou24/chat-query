from injector import singleton, inject

from exception import SystemException, ErrorCode
from modules.authority.application.member.dpo import MembersDpo
from modules.authority.domain.model.tenant import TenantId, TenantRepository


@singleton
class MemberApplicationService:
    @inject
    def __init__(self, tenant_repository: TenantRepository):
        self.tenant_repository = tenant_repository

    def members(self, tenant_id: str) -> MembersDpo:
        tenant_id = TenantId(tenant_id)
        tenant = self.tenant_repository.get(tenant_id)
        if tenant is None:
            raise SystemException(ErrorCode.TENANT_DOES_NOT_FOUND, f"テナント {tenant_id} が見つかりませんでした。")
        return MembersDpo(members=list(tenant.members))
