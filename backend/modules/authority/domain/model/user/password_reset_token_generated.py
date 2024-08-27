import datetime
from typing import override

from modules.authority.domain.model.user import UserId, Token, EmailAddress
from modules.common.domain.model import DomainEvent


class PasswordResetTokenGenerated(DomainEvent):
    user_id: UserId
    email_address: EmailAddress
    token: Token

    def __init__(self, user_id: UserId, email_address: EmailAddress, token: Token):
        super().__init__(1, datetime.datetime.now())
        super().__setattr__("user_id", user_id)
        super().__setattr__("email_address", email_address)
        super().__setattr__("token", token)

    @override
    def to_dict(self) -> dict:
        return {'user_id': self.user_id.value, 'email_address': self.email_address.text, 'token': self.token.value}
