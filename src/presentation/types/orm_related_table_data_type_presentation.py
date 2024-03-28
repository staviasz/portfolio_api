from typing_extensions import TypeVar, TypedDict, Type, Generic
from sqlalchemy.orm import DeclarativeBase

TOrm = TypeVar("TOrm", bound=DeclarativeBase)


class OrmRelatedTable(TypedDict, Generic[TOrm]):
    field_in_principal_table: str
    table_name: Type[TOrm]


class OrmRelatedTableData(OrmRelatedTable):
    data: list
    field_forengein_key: str
