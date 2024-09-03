import datetime
from dataclasses import dataclass
from typing import Any


@dataclass(init=True, unsafe_hash=True, frozen=True)
class Field:
    name: str
    semantic_type: type[str] | type[float] | type[int] | type[bool] | type[datetime.datetime] | type[datetime.date]


type Row = dict[str, Any]


@dataclass(init=True, unsafe_hash=True, frozen=True)
class DataSet:
    fields: list[Field]
    data_source: list[Row]
