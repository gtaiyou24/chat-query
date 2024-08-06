from __future__ import annotations

import uuid
from typing import override

from injector import inject

from modules.authority.domain.model.session import SessionRepository, SessionId, Session
from modules.authority.domain.model.user import UserId
from port.adapter.persistence.repository.mysql.session import CacheLayerSession


class MySQLSessionRepository(SessionRepository):
    @inject
    def __init__(self, cache_layer_session: CacheLayerSession):
        self.__cache_layer_session = cache_layer_session

    @override
    def next_identity(self) -> SessionId:
        return SessionId(str(uuid.uuid4()))

    @override
    def save(self, session: Session) -> None:
        self.__cache_layer_session.set(session)

    @override
    def remove(self, session: Session) -> None:
        self.__cache_layer_session.delete(session)

    @override
    def remove_all(self, *session: Session) -> None:
        for e in session:
            self.remove(e)

    @override
    def session_with_token(self, value: str) -> Session | None:
        return self.__cache_layer_session.cache_or_origin_with_token(value)

    @override
    def sessions_with_user_id(self, user_id: UserId) -> set[Session]:
        return self.__cache_layer_session.cache_or_origins_with_user_id(user_id)

    @override
    def get(self, session_id: SessionId) -> Session | None:
        return self.__cache_layer_session.cache_or_origin(session_id)
