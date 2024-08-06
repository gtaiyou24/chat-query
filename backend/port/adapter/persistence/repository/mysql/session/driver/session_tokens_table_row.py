from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Index, Integer, UniqueConstraint, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from modules.authority.domain.model.session import Session, Token
from port.adapter.persistence.repository.mysql import DataBase, EnumType

SessionTokenTypeField = Enum("Token.Type", " ".join([e.name for e in Token.Type]))


class SessionTokensTableRow(DataBase):
    __tablename__ = "session_tokens"
    __table_args__ = (
        (UniqueConstraint("value", name=f"uix_{__tablename__}_1")),
        (Index(f"idx_{__tablename__}_1", 'value')),
        (Index(f"idx_{__tablename__}_2", 'session_id')),
        (Index(f"idx_{__tablename__}_3", 'session_id', 'type')),
        {"mysql_charset": "utf8mb4", "mysql_engine": "InnoDB"}
    )

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, nullable=False, autoincrement=True)
    session_id: Mapped[str] = mapped_column(
        ForeignKey('sessions.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    type: Mapped[int] = mapped_column(
        EnumType(enum_class=SessionTokenTypeField), nullable=False, comment='1=アクセストークン, 2=リフレッシュトークン')
    value: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True, comment="発行されたトークンの文字列")
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="トークン発行日時")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="トークン失効日時")

    session = relationship("SessionsTableRow", back_populates="tokens")

    @staticmethod
    def create(session: Session) -> list[SessionTokensTableRow]:
        return [
            SessionTokensTableRow(
                session_id=session.id.value,
                type=SessionTokenTypeField[token.type.name],
                value=token.value,
                published_at=token.published_at,
                expires_at=token.expires_at
            ) for token in session.tokens
        ]

    def to_value(self) -> Token:
        return Token(Token.Type[self.type.name], self.value, self.published_at, self.expires_at)
