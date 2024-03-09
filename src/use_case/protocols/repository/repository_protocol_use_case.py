from typing_extensions import Protocol, TypeVar, Type

from sqlalchemy.orm import DeclarativeBase

from src.use_case.protocols.repository.get_by_email_repository_protocol_use_case import (
    GetByEmailRepositoryProtocolUseCase,
)
from src.use_case.protocols.repository.get_by_id_repository_protocol_use_case import (
    GetByIdRepositoryProtocolUseCase,
)

T = TypeVar("T", bound=DeclarativeBase)


class RepositoryProtocolUseCase(
    GetByEmailRepositoryProtocolUseCase, GetByIdRepositoryProtocolUseCase, Protocol
):
    async def get_all(self, table_name: Type[T]) -> list[dict]: ...

    async def create(self, table_name: Type[T], data: dict) -> dict: ...

    async def update(self, table_name: Type[T], data: dict, id: int) -> dict: ...

    async def delete(self, table_name: Type[T], id: int) -> None: ...
