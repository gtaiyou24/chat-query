from __future__ import annotations

from injector import inject
from typing import override

from modules.authority.domain.model.user.account import Account
from modules.authority.domain.model.user import UserRepository, User, UserId, EmailAddress
from port.adapter.persistence.repository.mysql.user import CacheLayerUser


class MySQLUserRepository(UserRepository):

    @inject
    def __init__(self, cache_layer_user: CacheLayerUser):
        self.__cache_layer_user = cache_layer_user

    @override
    def add(self, user: User) -> None:
        self.__cache_layer_user.set(user)

    @override
    def remove(self, user: User) -> None:
        self.__cache_layer_user.delete(user)

    @override
    def get(self, user_id: UserId) -> User | None:
        return self.__cache_layer_user.user_or_origin(user_id)

    @override
    def users_with_ids(self, *user_id: UserId) -> set[User]:
        return self.__cache_layer_user.users_or_origins(*user_id)

    @override
    def user_with_email_address(self, email_address: EmailAddress) -> User | None:
        return self.__cache_layer_user.user_or_origin_with_email_address(email_address)

    @override
    def user_with_account(self, provider: Account.Provider, provider_account_id: str) -> User | None:
        return self.__cache_layer_user.user_or_origin_with_account(provider, provider_account_id)

    @override
    def user_with_token(self, value: str) -> User | None:
        return self.__cache_layer_user.user_or_origin_with_token(value)
