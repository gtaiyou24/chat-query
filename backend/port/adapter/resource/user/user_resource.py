from di import DIContainer
from fastapi import APIRouter, Depends

from modules.authority.application.identity import IdentityApplicationService
from modules.authority.application.identity.dpo import UserDpo
from port.adapter.resource import APIResource
from port.adapter.resource.dependency import get_current_active_user
from port.adapter.resource.user.response import UserJson


class UserResource(APIResource):
    router = APIRouter(prefix="/users", tags=["ユーザー"])

    def __init__(self):
        self.__identity_application_service = None
        self.router.add_api_route("/me", self.me, methods=["GET"], response_model=UserJson)

    @property
    def identity_application_service(self) -> IdentityApplicationService:
        self.__identity_application_service = (
            self.__identity_application_service or
            DIContainer.instance().resolve(IdentityApplicationService)
        )
        return self.__identity_application_service

    def me(self, current_user: UserDpo = Depends(get_current_active_user)) -> UserJson:
        return UserJson.from_(current_user)
