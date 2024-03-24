from typing_extensions import Protocol, TypeVar, Type, Optional

from sqlalchemy.orm import DeclarativeBase

from src.presentation.types.orm_related_table_data_type_presentation import (
    OrmRelatedTableData,
    OrmRelatedTable,
)
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

    async def get_all(
        self, table_name: Type[T], filters: Optional[dict] = None
    ) -> list[dict]: ...

    async def create(
        self,
        table_name: Type[T],
        data: dict,
    ) -> dict: ...

    async def create_with_related(
        self,
        table_name: Type[T],
        data: dict,
        related_table: list[OrmRelatedTableData],
    ) -> dict: ...

    async def update(self, table_name: Type[T], data: dict, id: int) -> dict: ...

    async def update_with_related(
        self,
        table_name: Type[T],
        data: dict,
        related_table: list[OrmRelatedTableData],
        id: int,
    ) -> dict: ...

    async def delete(self, table_name: Type[T], id: int) -> None: ...

    async def delete_with_related(
        self, table_name: Type[T], id: int, related_table: list[OrmRelatedTable]
    ) -> None: ...
