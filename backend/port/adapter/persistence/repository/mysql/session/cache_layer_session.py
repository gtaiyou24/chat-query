from __future__ import annotations

from injector import inject, singleton

from modules.authority.domain.model.session import SessionId, Session
from modules.authority.domain.model.user import UserId
from port.adapter.persistence.repository.mysql.session import DriverManagerSession


@singleton
class CacheLayerSession:
    """キャッシュを保持するクラス"""
    values = dict()
    __TTL = 60 * 15  # 60秒 × 15分

    @inject
    def __init__(self, driver_manager_session: DriverManagerSession):
        self.__driver_manager_session = driver_manager_session

    def cache_or_origin(self, id: SessionId) -> Session | None:
        key = f'id-{id.value}'
        if key in self.values.keys():
            return self.values[key]

        optional = self.__driver_manager_session.find_by_id(id)
        self.values[key] = optional
        return self.values[key]

    def cache_or_origin_with_token(self, value: str) -> Session | None:
        return self.__driver_manager_session.find_by_token(value)

    def cache_or_origins_with_user_id(self, user_id: UserId) -> set[Session]:
        return set(self.__driver_manager_session.find_all_by(user_id=user_id.value))

    def set(self, session: Session) -> None:
        self.__driver_manager_session.upsert(session)
        # キャッシュを更新する
        self.values[f'id-{session.id.value}'] = session

    def delete(self, session: Session) -> None:
        self.__driver_manager_session.delete(session)
        # キャッシュを更新する
        self.values[f'id-{session.id.value}'] = None
