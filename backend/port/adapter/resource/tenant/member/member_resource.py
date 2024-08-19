from di import DIContainer
from fastapi import APIRouter, Depends

from exception import SystemException, ErrorCode
from modules.authority.application.identity.dpo import UserDpo
from modules.authority.application.member import MemberApplicationService
from port.adapter.resource import APIResource
from port.adapter.resource.dependency import get_current_active_user
from port.adapter.resource.tenant.member.request import ChangeRoleRequest, InviteMemberRequest
from port.adapter.resource.tenant.member.response import MemberListJson, MemberJson


class MemberResource(APIResource):
    router = APIRouter(prefix="/tenants/{tenant_id}/members", tags=["Members"])

    def __init__(self):
        self.__member_application_service = None
        self.router.add_api_route("", self.members, methods=["GET"], response_model=MemberListJson)
        self.router.add_api_route("/invite", self.invite, methods=["POST"])
        self.router.add_api_route("/join", self.join, methods=["POST"])
        self.router.add_api_route("/{member_id}", self.change, methods=["PUT"], response_model=MemberJson)
        self.router.add_api_route("/{member_id}", self.remove, methods=["DELETE"], response_model=MemberListJson)

    @property
    def member_application_service(self) -> MemberApplicationService:
        self.__member_application_service = (
            self.__member_application_service or DIContainer.instance().resolve(MemberApplicationService)
        )
        return self.__member_application_service

    def members(self, tenant_id: str, current_user_dpo: UserDpo = Depends(get_current_active_user)) -> MemberListJson:
        if not current_user_dpo.has_tenant(tenant_id):
            raise SystemException(ErrorCode.TENANT_DOES_NOT_FOUND, f"テナント {tenant_id} が見つかりませんでした。")
        dpo = self.member_application_service.members(tenant_id)
        return MemberListJson.from_(dpo)

    def invite(self,
               tenant_id: str,
               request: InviteMemberRequest,
               current_user_dpo: UserDpo = Depends(get_current_active_user)) -> None:
        pass

    def join(self, tenant_id: str, current_user_dpo: UserDpo = Depends(get_current_active_user)) -> None:
        pass

    def change(self,
               tenant_id: str,
               member_id: str,
               request: ChangeRoleRequest,
               current_user_dpo: UserDpo = Depends(get_current_active_user)) -> MemberJson:
        pass

    def remove(self,
               tenant_id: str,
               member_id: str,
               current_user_dpo: UserDpo = Depends(get_current_active_user)) -> MemberListJson:
        pass
