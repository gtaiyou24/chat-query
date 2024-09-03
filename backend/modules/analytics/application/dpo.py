from dataclasses import dataclass

from modules.analytics.domain.model.database import DataSet


@dataclass(init=True, unsafe_hash=True, frozen=True)
class DataSetDpo:
    query: str
    dataset: DataSet
