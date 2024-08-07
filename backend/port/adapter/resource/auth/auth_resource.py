from di import DIContainer
from fastapi import APIRouter

from exception import SystemException, ErrorCode
from modules.authority.application.identity import IdentityApplicationService
from modules.authority.application.identity.command import ProvisionTenantCommand, AuthenticateUserCommand
from port.adapter.resource import APIResource
from port.adapter.resource.auth.request import RegisterTenantRequest, OAuth2PasswordRequest
from port.adapter.resource.auth.response import TokenJson


class AuthResource(APIResource):
    router = APIRouter(prefix="/auth", tags=["認証"])

    def __init__(self):
        self.__identity_application_service = None
        self.router.add_api_route("/register", self.register, methods=["POST"], name="ユーザー登録")
        self.router.add_api_route("/unregister", self.unregister, methods=["DELETE"], name="ユーザー削除")
        self.router.add_api_route("/verify-email/{token}", self.verify_email, methods=["POST"], name='メールアドレス検証')
        self.router.add_api_route("/token", self.token, methods=["POST"], response_model=TokenJson, name='トークンを発行')
        self.router.add_api_route("/forgot-password", self.forgot_password, methods=["POST"], name='パスワードリセット')
        self.router.add_api_route("/reset-password", self.reset_password, methods=["POST"], name='パスワード再設定')
        self.router.add_api_route("/change-password", self.change_password, methods=["POST"], name="パスワード更新")

    @property
    def identity_application_service(self) -> IdentityApplicationService:
        self.__identity_application_service = (
            self.__identity_application_service or DIContainer.instance().resolve(IdentityApplicationService)
        )
        return self.__identity_application_service

    def register(self, request: RegisterTenantRequest) -> None:
        """ユーザー登録"""
        command = ProvisionTenantCommand(
            ProvisionTenantCommand.Tenant(request.username),
            ProvisionTenantCommand.User(request.username, request.email_address, request.password)
        )
        self.identity_application_service.provision_tenant(command)

    def unregister(self) -> None:
        """ユーザー削除"""
        pass

    def verify_email(self, token: str) -> None:
        """メールアドレス検証"""
        self.identity_application_service.verify_email(token)

    def token(self, request: OAuth2PasswordRequest) -> TokenJson:
        """トークンを発行"""
        command = AuthenticateUserCommand(request.email_address, request.password)
        dpo = self.identity_application_service.authenticate(command)
        if dpo is None:
            raise SystemException(ErrorCode.USER_IS_NOT_VERIFIED, "メールアドレスの検証が完了していません。確認メールを送信しました。")
        return TokenJson.from_(dpo)

    def forgot_password(self) -> None:
        pass

    def reset_password(self) -> None:
        pass

    def change_password(self) -> None:
        pass
