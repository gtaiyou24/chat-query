from injector import singleton, inject

from exception import SystemException, ErrorCode
from modules.authority.application.tenant.dpo import TenantListDpo, ProjectListDpo
from modules.authority.domain.model.tenant import TenantRepository, TenantId
from modules.authority.domain.model.tenant.project import ProjectRepository
from modules.authority.domain.model.user import UserId


@singleton
class TenantApplicationService:
    @inject
    def __init__(self,
                 tenant_repository: TenantRepository,
                 project_repository: ProjectRepository):
        self.tenant_repository = tenant_repository
        self.project_repository = project_repository

    def tenants(self, user_id: str) -> TenantListDpo:
        user_id = UserId(user_id)
        tenants = self.tenant_repository.tenants_with_user_id(user_id)
        return TenantListDpo(tenants=tenants)

    def projects(self, user_id: str, tenant_id: str) -> ProjectListDpo:
        user_id = UserId(user_id)
        tenant_id = TenantId(tenant_id)
        tenant = self.tenant_repository.get(tenant_id)
        if not tenant.has_member(user_id):
            raise SystemException(ErrorCode.TENANT_DOES_NOT_FOUND, f"テナント {tenant_id} は見つかりませんでした。")
        projects = self.project_repository.projects_with_tenant_id(tenant_id)
        return ProjectListDpo(projects=list(projects))
