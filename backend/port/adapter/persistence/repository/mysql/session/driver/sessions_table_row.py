from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modules.authority.domain.model.session import Session, SessionId
from modules.authority.domain.model.user import UserId
from port.adapter.persistence.repository.mysql import DataBase
from port.adapter.persistence.repository.mysql.session.driver import SessionTokensTableRow


class SessionsTableRow(DataBase):
    __tablename__ = "sessions"
    __table_args__ = (
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, comment="UUID")
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),
                                                 comment="作成日時")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 comment="更新日時")

    tokens: Mapped[list[SessionTokensTableRow]] = relationship(back_populates="session", lazy='joined')

    @staticmethod
    def create(session: Session) -> SessionsTableRow:
        return SessionsTableRow(
            id=session.id.value,
            user_id=session.user_id.value,
            tokens=SessionTokensTableRow.create(session)
        )

    def update(self, session: Session) -> None:
        self.user_id = session.user_id.value
        self.tokens = SessionTokensTableRow.create(session)

    def to_entity(self) -> Session:
        return Session(
            id=SessionId(self.id),
            user_id=UserId(self.user_id),
            tokens={tr.to_value() for tr in self.tokens}
        )
