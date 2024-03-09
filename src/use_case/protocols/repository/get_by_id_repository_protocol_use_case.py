from typing_extensions import Protocol, TypeVar, Type
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound="DeclarativeBase")


class GetByIdRepositoryProtocolUseCase(Protocol):

    async def get_by_id_instace(self, table_name: Type[T], id: int) -> T: ...

    async def get_by_id_dict(self, table_name: Type[T], id: int) -> dict: ...
