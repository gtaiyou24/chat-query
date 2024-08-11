from fastapi import APIRouter, Depends

from modules.authority.application.identity.dpo import UserDpo
from port.adapter.resource import APIResource
from port.adapter.resource.dependency import get_current_active_user
from port.adapter.resource.tenant.member.request import ChangeRoleRequest, InviteMemberRequest
from port.adapter.resource.tenant.member.response import MemberListJson, MemberJson


class MemberResource(APIResource):
    router = APIRouter(prefix="/tenants/{tenant_id}/members", tags=["Members"])

    def __init__(self):
        self.router.add_api_route("", self.members, methods=["GET"], response_model=MemberListJson)
        self.router.add_api_route("", self.invite, methods=["POST"])
        self.router.add_api_route("/{member_id}", self.change, methods=["PUT"], response_model=MemberJson)
        self.router.add_api_route("/{member_id}", self.remove, methods=["DELETE"], response_model=MemberListJson)

    def members(self, tenant_id: str, current_user_dpo: UserDpo = Depends(get_current_active_user)) -> MemberListJson:
        pass

    def invite(self,
               tenant_id: str,
               request: InviteMemberRequest,
               current_user_dpo: UserDpo = Depends(get_current_active_user)) -> None:
        pass

    def change(self,
               tenant_id: str,
               member_id: str,
               request: ChangeRoleRequest,
               current_user_dpo: UserDpo = Depends(get_current_active_user)) -> MemberJson:
        pass

    def remove(self, tenant_id: str, member_id: str, current_user_dpo: UserDpo = Depends(get_current_active_user)) -> MemberListJson:
        pass
