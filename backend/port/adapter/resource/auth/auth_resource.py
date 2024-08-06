from fastapi import APIRouter

from port.adapter.resource import APIResource


class AuthResource(APIResource):
    router = APIRouter(prefix="/auth")

    def __init__(self):
        self.router.add_api_route("/register", self.register, methods=["POST"], name="ユーザー登録")
        self.router.add_api_route("/unregister", self.unregister, methods=["DELETE"], name="ユーザー削除")
        self.router.add_api_route("/verify-email/{token}", self.verify_email, methods=["POST"], name='メールアドレス検証')
        self.router.add_api_route("/forgot-password", self.forgot_password, methods=["POST"], name='パスワードリセット')
        self.router.add_api_route("/reset-password", self.reset_password, methods=["POST"], name='パスワード再設定')
        self.router.add_api_route("/change-password", self.change_password, methods=["POST"], name="パスワード更新")

    def register(self) -> None:
        """ユーザー登録"""
        pass

    def unregister(self) -> None:
        """ユーザー削除"""
        pass

    def verify_email(self, token: str) -> None:
        """メールアドレス検証"""
        pass

    def forgot_password(self) -> None:
        pass

    def reset_password(self) -> None:
        pass

    def change_password(self) -> None:
        pass
