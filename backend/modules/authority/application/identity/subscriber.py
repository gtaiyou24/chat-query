import os

from modules.authority.domain.model.mail import SendMailService
from modules.authority.domain.model.user import UserProvisioned, UserRepository, Token
from modules.common.domain.model import DomainEventSubscriber, DomainRegistry


class UserProvisionedSubscriber(DomainEventSubscriber[UserProvisioned]):
    """ユーザー作成イベントを購読するサブスクライバ"""
    def __init__(self):
        self.send_mail_service = DomainRegistry.resolve(SendMailService)
        self.user_repository = DomainRegistry.resolve(UserRepository)

    def handle_event(self, domain_event: UserProvisioned) -> None:
        """メアド確認のための検証メールを送信する"""
        user = self.user_repository.get(domain_event.user_id)
        if user is None:
            raise ValueError(f"ユーザー {domain_event.user_id.value} が存在しないため、検証メールを送信できません。"
                             f"そのため、ユーザー {domain_event.user_id.value} は非アクティブ状態です。")

        token = user.latest_token_of(Token.Type.VERIFICATION)
        self.send_mail_service.send(
            user.email_address,
            '【Analytics GPT】メールアドレスの検証',
            f"""<html>
            <body>
            <h1>メールアドレスの確認をします</h1>
            <a href="{os.getenv('FRONTEND_URL')}/auth/new-verification?token={token.value}">
                こちらをクリックしてください。
            </a>
            </body>
            </html>""")