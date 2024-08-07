import os
from typing import override

from modules.authority.domain.model.mail import SendMailService
from modules.authority.domain.model.user import VerificationTokenGenerated, UserRepository
from modules.common.domain.model import DomainEventSubscriber, DomainRegistry


class UserProvisionedSubscriber(DomainEventSubscriber[VerificationTokenGenerated]):
    """ユーザー作成イベントを購読するサブスクライバ"""
    def __init__(self):
        self.send_mail_service = DomainRegistry.resolve(SendMailService)
        self.user_repository = DomainRegistry.resolve(UserRepository)

    @override
    def subscribed_to_event_type(self) -> type[VerificationTokenGenerated]:
        return VerificationTokenGenerated

    @override
    def handle_event(self, domain_event: VerificationTokenGenerated) -> None:
        """メアド確認のための検証メールを送信する"""
        try:
            self.send_mail_service.send(
                domain_event.email_address,
                '【Analytics GPT】メールアドレスの検証',
                f"""<html>
                <body>
                <h1>メールアドレスの確認をします</h1>
                <a href="{os.getenv('FRONTEND_URL')}/auth/new-verification?token={domain_event.token.value}">
                    こちらをクリックしてください。
                </a>
                </body>
                </html>""")
        except Exception as e:
            raise ValueError(f"ユーザー {domain_event.user_id.value} 宛の検証メールを送信できませんでした。{e}")
