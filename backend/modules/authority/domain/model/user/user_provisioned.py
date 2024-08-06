import datetime
from typing import override

from modules.authority.domain.model.user import UserId
from modules.common.domain.model import DomainEvent


class UserProvisioned(DomainEvent):
    user_id: UserId

    def __init__(self, user_id: UserId):
        super().__init__(1, datetime.datetime.now())
        super().__setattr__("user_id", user_id)

    @override
    def to_dict(self) -> dict:
        return {'user_id': self.user_id.value}