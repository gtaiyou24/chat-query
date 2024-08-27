from injector import singleton, inject

from exception import SystemException, ErrorCode
from modules.authority.application.member.dpo import MembersDpo
from modules.authority.domain.model.tenant import TenantId, TenantRepository
from modules.authority.domain.model.user import UserRepository


@singleton
class MemberApplicationService:
    @inject
    def __init__(self,
                 tenant_repository: TenantRepository,
                 user_repository: UserRepository):
        self.tenant_repository = tenant_repository
        self.user_repository = user_repository

    def members(self, tenant_id: str) -> MembersDpo:
        tenant_id = TenantId(tenant_id)
        tenant = self.tenant_repository.get(tenant_id)
        if tenant is None:
            raise SystemException(ErrorCode.TENANT_DOES_NOT_FOUND, f"テナント {tenant_id} が見つかりませんでした。")
        users = self.user_repository.users_with_ids(*tenant.member_user_ids)
        return MembersDpo(members=list(tenant.members), users=users)
