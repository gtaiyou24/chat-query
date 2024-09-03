from typing import override

from injector import inject

from modules.analytics.domain.model.database import DataBaseService, DataSet
from port.adapter.service.database.adapter import DataBaseAdapter


class DataBaseServiceImpl(DataBaseService):
    @inject
    def __init__(self, database_dapter: DataBaseAdapter):
        self.__database_dapter = database_dapter

    @override
    def schemas(self) -> list[str]:
        return self.__database_dapter.schemas()

    @override
    def query(self, query: str) -> DataSet | None:
        return self.__database_dapter.query(query)
