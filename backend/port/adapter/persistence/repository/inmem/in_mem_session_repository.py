from __future__ import annotations

import uuid
from typing import override

from modules.authority.domain.model.session import SessionRepository, SessionId, Session
from modules.authority.domain.model.user import UserId


class InMemSessionRepository(SessionRepository):
    __values: set[Session] = set()

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
    def remove_all(self, *session: Session) -> None:
        [self.__values.remove(e) for e in session]

    @override
    def session_with_token(self, value: str) -> Session | None:
        for session in self.__values:
            if session.token_with(value):
                return session
        return None

    @override
    def sessions_with_user_id(self, user_id: UserId) -> set[Session]:
        user_sessions = set()
        for session in self.__values:
            if session.user_id == user_id:
                user_sessions.add(session)
        return user_sessions

    @override
    def get(self, session_id: SessionId) -> Session | None:
        for session in self.__values:
            if session.id == session_id:
                return session
        return None
