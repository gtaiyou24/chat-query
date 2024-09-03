import abc

from modules.analytics.domain.model.database import DataSet


class DataBaseService(abc.ABC):
    @abc.abstractmethod
    def schemas(self) -> list[str]:
        pass

    @abc.abstractmethod
    def query(self, query: str) -> DataSet | None:
        pass
