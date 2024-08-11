from di import DIContainer
from fastapi import APIRouter, Depends

from modules.authority.application.identity.dpo import UserDpo
from modules.authority.application.tenant import TenantApplicationService
from port.adapter.resource import APIResource
from port.adapter.resource.dependency import get_current_active_user
from port.adapter.resource.tenant.response import TenantListJson, ProjectListJson


class TenantResource(APIResource):
    router = APIRouter(prefix="/tenants", tags=["テナント"])

    def __init__(self):
        self.__tenant_application_service = None
        self.router.add_api_route("/", self.tenants, methods=["GET"], response_model=TenantListJson)
        self.router.add_api_route(
            "/{tenant_id}/projects", self.projects, methods=["GET"], response_model=ProjectListJson)

    @property
    def tenant_application_service(self) -> TenantApplicationService:
        self.__tenant_application_service = (
            self.__tenant_application_service or DIContainer.instance().resolve(TenantApplicationService)
        )
        return self.__tenant_application_service

    def tenants(self, current_user_dpo: UserDpo = Depends(get_current_active_user)) -> TenantListJson:
        dpo = self.tenant_application_service.tenants(current_user_dpo.user.id.value)
        return TenantListJson.from_(dpo)

    def projects(self, tenant_id: str, current_user_dpo: UserDpo = Depends(get_current_active_user)) -> ProjectListJson:
        dpo = self.tenant_application_service.projects(current_user_dpo.user.id.value, tenant_id)
        return ProjectListJson.from_(dpo)
