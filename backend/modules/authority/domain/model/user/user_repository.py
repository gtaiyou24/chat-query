from __future__ import annotations

import abc
import uuid

from modules.authority.domain.model.user import User, UserId, EmailAddress
from modules.authority.domain.model.user.account import Account


class UserRepository(abc.ABC):
    def next_identity(self) -> UserId:
        return UserId(str(uuid.uuid4()))

    @abc.abstractmethod
    def add(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def remove(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def get(self, user_id: UserId) -> User | None:
        pass

    @abc.abstractmethod
    def users_with_ids(self, *user_id: UserId) -> set[User]:
        pass

    @abc.abstractmethod
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        pass

    @abc.abstractmethod
    def user_with_account(self, provider: Account.Provider, provider_account_id: str) -> User | None:
        pass

    @abc.abstractmethod
    def user_with_token(self, value: str) -> User | None:
        pass
