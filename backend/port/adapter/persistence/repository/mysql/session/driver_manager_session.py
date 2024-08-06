from __future__ import annotations

from injector import inject

from modules.common.application import UnitOfWork
from modules.authority.domain.model.session import Session, SessionId
from port.adapter.persistence.repository.mysql import MySQLUnitOfWork
from port.adapter.persistence.repository.mysql.session.driver import SessionsTableRow, SessionTokensTableRow


class DriverManagerSession:
    @inject
    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work: MySQLUnitOfWork = unit_of_work

    def find_by_id(self, id: SessionId) -> Session | None:
        with self.__unit_of_work.query() as q:
            optional: SessionsTableRow | None = q.query(SessionsTableRow).get(id.value)
            return optional.to_entity() if optional else None

    def find_one_by(self, **kwargs) -> Session | None:
        with self.__unit_of_work.query() as q:
            optional: SessionsTableRow | None = q.query(SessionsTableRow).filter_by(**kwargs).one_or_none()
            if optional is None:
                return None
            return optional.to_entity()

    def find_all_by(self, **kwargs) -> list[Session]:
        with self.__unit_of_work.query() as q:
            all: list[SessionsTableRow] = q.query(SessionsTableRow).filter_by(**kwargs).all()
            return [e.to_entity() for e in all]

    def find_by_token(self, value: str) -> Session | None:
        with self.__unit_of_work.query() as q:
            one: SessionTokensTableRow | None = q.query(SessionTokensTableRow).filter_by(value=value).one_or_none()
            if one is None:
                return None
            return one.session.to_entity()

    def upsert(self, session: Session) -> None:
        optional: SessionsTableRow | None = self.__unit_of_work.session().query(SessionsTableRow).get(session.id.value)
        if optional is not None:
            self.update(session)
        else:
            self.insert(session)

    def insert(self, session: Session) -> None:
        self.__unit_of_work.persist(SessionsTableRow.create(session))

    def update(self, session: Session) -> None:
        optional: SessionsTableRow | None = self.__unit_of_work.session().query(SessionsTableRow).get(session.id.value)
        if optional is None:
            raise Exception(f'{SessionsTableRow.__tablename__}.{session.id.value} が存在しないため、更新できません。')

        self.__unit_of_work.delete(*optional.tokens)
        self.__unit_of_work.flush()

        optional.update(session)

    def delete(self, session: Session) -> None:
        optional: SessionsTableRow | None = self.__unit_of_work.session().query(SessionsTableRow).get(session.id.value)
        if optional is None:
            return None

        self.__unit_of_work.delete(*optional.tokens)
        self.__unit_of_work.flush()

        self.__unit_of_work.delete(optional)
