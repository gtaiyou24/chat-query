from __future__ import annotations

import uuid
from typing import override

from modules.authority.domain.model.session import SessionRepository, SessionId, Session


class InMemSessionRepository(SessionRepository):
    __values = set()

    @override
    def next_identity(self) -> SessionId:
        return SessionId(str(uuid.uuid4()))

    @override
    def save(self, session: Session) -> None:
        self.__values.add(session)

    @override
    def remove(self, session: Session) -> None:
        self.__values.remove(session)

    @override
    def session_with_token(self, value: str) -> Session | None:
        for session in self.__values:
            if session.token_with(value):
                return session
        return None

    @override
    def get(self, session_id: SessionId) -> Session | None:
        for session in self.__values:
            if session.id == session_id:
                return session
        return None
